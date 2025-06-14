from queue import PriorityQueue
from geopy.distance import geodesic
import pandas as pd
from joblib import load
from datetime import datetime

from clients.here_traffic_client import TrafficClient
from clients.open_weather_client import WeatherClient


# Constants
MAX_DISTANCE_MILES = 10
MAX_CO2_PER_MILE = 0.5
MAX_AVERAGE_PAY = 20
MAX_TRAFFIC_DELAY_MIN = 60

# ---- Model Components ---- #

MODEL = load("model/driver_acceptance_model.pkl")

# Ordered feature list (from the trained model)
MODEL_FEATURES = [
    "distance_to_pickup_mi",
    "dropoff_distance_mi",
    "delivery_size_lbs",
    "offered_pay_usd",
    "acceptance_rate_7d",
    "acceptance_rate_14d",
    "acceptance_rate_30d",
    "reliability_score",
    "traffic_delay_min",
    "weather_delay_factor",
    "hour_of_day",
    "day_of_week",
    # One-hot encoded vehicle types (modify based on training data) -> diesel is dropped
    "vehicle_type_electric",
    "vehicle_type_hybrid",
    "vehicle_type_petrol",
]


def to_feature_vector(driver, delivery, pay=15.0):
    now = datetime.now()
    vehicle_onehot = {
        "vehicle_type_electric": 1 if driver["vehicle_type"] == "electric" else 0,
        "vehicle_type_hybrid": 1 if driver["vehicle_type"] == "hybrid" else 0,
        "vehicle_type_petrol": 1 if driver["vehicle_type"] == "petrol" else 0,
    }

    feature_dict = {
        "distance_to_pickup_mi": geodesic(
            (delivery["pickup_lat"], delivery["pickup_lon"]),
            (driver["lat"], driver["lon"]),
        ).miles,
        "dropoff_distance_mi": geodesic(
            (delivery["drop_lat"], delivery["drop_lon"]), (driver["lat"], driver["lon"])
        ).miles,
        "delivery_size_lbs": delivery["size_lbs"],
        "offered_pay_usd": pay,
        "acceptance_rate_7d": driver.get("acceptance_last_7_days", 0),
        "acceptance_rate_14d": driver.get("acceptance_last_14_days", 0),
        "acceptance_rate_30d": driver.get("acceptance_last_30_days", 0),
        "reliability_score": driver["reliability"],
        "traffic_delay_min": delivery.get("traffic_delay_min", 0),
        "weather_delay_factor": delivery.get("weather_delay_factor", 0),
        "hour_of_day": now.hour,
        "day_of_week": now.weekday(),
        **vehicle_onehot,
    }

    return [feature_dict.get(f, 0) for f in MODEL_FEATURES]


def model_acceptance_prob(driver: dict, delivery: dict, pay: float = 15.0) -> float:
    features = to_feature_vector(driver, delivery, pay)
    df = pd.DataFrame([features], columns=MODEL_FEATURES)
    return MODEL.predict_proba(df)[0][1]


def choose_best_driver_with_tiebreak(drivers, delivery, threshold=0.05):
    """
    Rank drivers by score, then use ML model to break ties within a close score threshold.
    Returns the (score, best driver) tuple.
    """
    driver_score_map = []
    for driver in drivers:
        if is_eligible(driver, delivery):
            score = compute_total_score(driver, delivery)
            driver_score_map.append({"driver": driver, "score": score})

    if not driver_score_map:
        return None

    driver_score_map.sort(key=lambda x: x["score"], reverse=True)

    top_score = driver_score_map[0]["score"]
    tie_band = [
        entry
        for entry in driver_score_map
        if abs(entry["score"] - top_score) <= threshold
    ]

    if len(tie_band) == 1:
        return top_score, tie_band[0]["driver"]

    for entry in tie_band:
        entry["accept_prob"] = model_acceptance_prob(entry["driver"], delivery)

    tie_band.sort(key=lambda x: x["accept_prob"], reverse=True)

    return tie_band[0]["score"], tie_band[0]["driver"]


# ---- Scoring Components ---- #


def get_distance_miles(driver, delivery):
    return geodesic(
        (delivery["pickup_lat"], delivery["pickup_lon"]), (driver["lat"], driver["lon"])
    ).miles


def distance_score(driver, delivery):
    distance = get_distance_miles(driver, delivery)
    return max(0, 1 - (distance / MAX_DISTANCE_MILES))


def calculate_CO2_per_mile(driver):
    if driver["vehicle_type"] in [
        "petrol",
        "diesel",
        "hybrid",
    ]:  # hybrid is in the same class b/c similar emissions, you just
        #  get a better mileage
        emission_factor = 8.91 if driver["vehicle_type"] != "diesel" else 10.16
        return (
            (1 / driver["mpg"]) * emission_factor if driver["mpg"] else MAX_CO2_PER_MILE
        )

    if driver["vehicle_type"] in ["electric", "bike"]:
        kWh_per_mile = (driver["kWh_per_100km"] / 100) * 1.609
        return kWh_per_mile * 0.4
    return MAX_CO2_PER_MILE


def sustainability_score(driver):
    co2 = calculate_CO2_per_mile(driver)
    return max(0, 1 - (co2 / MAX_CO2_PER_MILE))


def reliability_score(driver):
    return min(driver["reliability"] / 100, 1)


def effective_acceptance_rate_score(driver):
    """
    Calculates the effective acceptance score. We use a decay-weighted acceptance scorer
    and a redemption based bonus if acceptance rate has improved over the past week.
    """
    effective_score = (
        0.6
        * (
            driver.get("acceptance_last_7_days", 0)
        )  # fallback if driver is new to the program
        + 0.3 * (driver.get("acceptance_last_14_days", 0))
        + 0.1 * (driver.get("acceptance_last_30_days", 0))
    ) / 100

    # Trend bonus if they've improved week-over-week
    if driver["acceptance_last_7_days"] > driver["acceptance_last_14_days"]:
        effective_score += 0.02

    return min(effective_score, 1)


def cost_score(driver):
    return max(0, 1 - (driver["average_pay"] / MAX_AVERAGE_PAY))


def traffic_score(delivery):
    return max(0, 1 - (delivery.get("traffic_delay_min", 0) / MAX_TRAFFIC_DELAY_MIN))


def weather_score(delivery):
    # 0 (perfect conditions) to 1 (heavy rain/storm etc)
    delay_factor = delivery.get("weather_delay_factor", 0)
    return max(0, 1 - delay_factor)


# ---- Eligibility check for delivery ---- #


def is_eligible(driver, delivery):
    """
    Return `True` if a driver fulfils eligibility criteria for a particular delivery.
    """
    if (
        get_distance_miles(driver, delivery) > MAX_DISTANCE_MILES
        or driver["capacity_lbs"] < delivery["size_lbs"]
        or not driver["available"]
    ):
        return False

    return True


# ---- Total Score Computation ---- #


def compute_total_score(driver, delivery):
    """
    Compute total score. Weights are subject to change.

    - Promote consistent, responsible drivers
    - Encourage comebacks
    - Still respect proximity and cost
    - Let sustainability matter, without dominating
    """

    weights = {
        "distance": 0.20,
        "sustainability": 0.10,
        "reliability": 0.25,
        "acceptance": 0.25,
        "cost": 0.10,
        "traffic": 0.07,
        "weather": 0.03,
    }

    scores = {
        "distance": distance_score(driver, delivery),
        "sustainability": sustainability_score(driver),
        "reliability": reliability_score(driver),
        "acceptance": effective_acceptance_rate_score(driver),
        "cost": cost_score(driver),
        "traffic": traffic_score(
            delivery
        ),  # change to driver once real data is available
        "weather": weather_score(delivery),
    }

    total = sum(scores[k] * weights[k] for k in weights)
    return round(total, 4)


# Sample usage
if __name__ == "__main__":
    import pprint
    from sample_data.orlando_fl import DRIVERS, DELIVERIES
    from dotenv import load_dotenv
    import os

    load_dotenv()

    # Initialize clients
    traffic_client = TrafficClient(api_key=os.getenv("HERE_API_KEY"))
    weather_client = WeatherClient(api_key=os.getenv("OPEN_WEATHER_API_KEY"))
    # Update deliveries with traffic and weather data
    for delivery in DELIVERIES:
        delivery["traffic_delay_min"] = traffic_client.get_traffic_delay_minutes(
            delivery["pickup_lat"],
            delivery["pickup_lon"],
            delivery["drop_lat"],
            delivery["drop_lon"],
        )
        delivery["weather_delay_factor"] = weather_client.get_weather_delay_factor(
            delivery["drop_lat"], delivery["drop_lon"]
        )

    # Example usage
    for delivery in DELIVERIES:
        result = choose_best_driver_with_tiebreak(DRIVERS, delivery)
        if result:
            score, best_driver = result
            print("Best driver:")
            pprint.pprint(best_driver)
            print("Score:", round(score, 4))
