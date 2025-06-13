from queue import PriorityQueue
from geopy.distance import geodesic

# Constants
MAX_DISTANCE_MILES = 10
MAX_CO2_PER_MILE = 0.5
MAX_AVERAGE_PAY = 20
MAX_TRAFFIC_DELAY_MIN = 60

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


def choose_best_driver(drivers, delivery):
    pq = PriorityQueue()
    for driver in drivers:
        if not is_eligible(driver, delivery):
            continue

        score = compute_total_score(driver, delivery)
        if score > 0:
            pq.put((-score, driver))  # negative score for max heap
    return pq.get() if not pq.empty() else None


if __name__ == "__main__":
    import pprint
    from sample_data.orlando_fl import DRIVERS, DELIVERIES

    # Example usage
    for delivery in DELIVERIES:
        score, best_driver = choose_best_driver(DRIVERS, delivery)
        if best_driver:
            print("Best driver:")
            pprint.pprint(best_driver)
            print(-score)
