# -----------------------
# Generate Mock Data
# -----------------------
import random
import pandas as pd 
from score.scoring_algorithm import compute_total_score

random.seed(42)

vehicle_types = ["petrol", "diesel", "electric", "hybrid"]
drivers = []

for i in range(30):
    vtype = random.choice(vehicle_types)
    mpg = random.randint(18, 35) if vtype in ["petrol", "diesel", "hybrid"] else None
    kwh = random.randint(13, 20) if vtype in ["electric"] else None
    driver = {
        "id": f"d{i+1}",
        "lat": 28.53 + random.uniform(-0.01, 0.01),
        "lon": -81.38 + random.uniform(-0.01, 0.01),
        "vehicle_type": vtype,
        "mpg": mpg,
        "kWh_per_100km": kwh,
        "acceptance_last_7_days": random.randint(60, 95),
        "acceptance_last_14_days": random.randint(55, 90),
        "acceptance_last_30_days": random.randint(50, 85),
        "reliability": random.randint(70, 99),
        "average_pay": random.uniform(12, 18),
        "capacity_lbs": random.randint(10, 50),
        "available": random.choice([True, True, False])
    }
    drivers.append(driver)

deliveries = [
    {
        "id": "order_1",
        "pickup_lat": 28.5383,
        "pickup_lon": -81.3792,
        "drop_lat": 28.5411,
        "drop_lon": -81.3888,
        "size_lbs": random.choice([10, 20, 30, 40]),
        "traffic_delay_min": random.choice([3, 5, 10, 15]),
        "weather_delay_factor": random.choice([0.0, 0.1, 0.2, 0.3])
    }
]

# -----------------------
# Evaluate & Aggregate
# -----------------------

results = []
for delivery in deliveries:
    for driver in drivers:
        if not driver["available"]:
            continue
        score = compute_total_score(driver, delivery)
        results.append({
            "driver_id": driver["id"],
            "vehicle_type": driver["vehicle_type"],
            "score": score
        })

results_df = pd.DataFrame(results).sort_values(by="score", ascending=False)
results_df.head(10)  
