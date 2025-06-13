WALMART_STORE = {
    "id": "store_001",
    "name": "Walmart Supercenter, Austin TX",
    "pickup_lat": 30.3540,
    "pickup_lon": -97.7031
}

DRIVERS = [
    {
        "id": "d1", "lat": 30.3512, "lon": -97.7005, "vehicle_type": "electric",
        "mpg": None, "kWh_per_100km": 14, "acceptance_rate": 90,
        "reliability": 98, "average_pay": 13.5, "capacity_lbs": 40, "available": True
    },
    {
        "id": "d2", "lat": 30.3495, "lon": -97.7053, "vehicle_type": "petrol",
        "mpg": 28, "kWh_per_100km": None, "acceptance_rate": 65,
        "reliability": 85, "average_pay": 17, "capacity_lbs": 25, "available": False
    },
    {
        "id": "d3", "lat": 30.3575, "lon": -97.7022, "vehicle_type": "hybrid",
        "mpg": 45, "kWh_per_100km": None, "acceptance_rate": 88,
        "reliability": 91, "average_pay": 14, "capacity_lbs": 20, "available": True
    },
    {
        "id": "d4", "lat": 30.3601, "lon": -97.6991, "vehicle_type": "electric",
        "mpg": None, "kWh_per_100km": 16, "acceptance_rate": 70,
        "reliability": 75, "average_pay": 15.5, "capacity_lbs": 50, "available": True
    },
    {
        "id": "d5", "lat": 30.3650, "lon": -97.7089, "vehicle_type": "diesel",
        "mpg": 20, "kWh_per_100km": None, "acceptance_rate": 60,
        "reliability": 82, "average_pay": 16.5, "capacity_lbs": 18, "available": True
    },
    {
        "id": "d6", "lat": 30.3680, "lon": -97.7122, "vehicle_type": "bike",
        "mpg": None, "kWh_per_100km": 10, "acceptance_rate": 95,
        "reliability": 99, "average_pay": 12.5, "capacity_lbs": 10, "available": False
    },
    {
        "id": "d7", "lat": 30.3533, "lon": -97.6905, "vehicle_type": "petrol",
        "mpg": 30, "kWh_per_100km": None, "acceptance_rate": 76,
        "reliability": 88, "average_pay": 13, "capacity_lbs": 35, "available": True
    },
    {
        "id": "d8", "lat": 30.3401, "lon": -97.6993, "vehicle_type": "electric",
        "mpg": None, "kWh_per_100km": 18, "acceptance_rate": 80,
        "reliability": 94, "average_pay": 15, "capacity_lbs": 22, "available": True
    },
    {
        "id": "d9", "lat": 30.3430, "lon": -97.7155, "vehicle_type": "hybrid",
        "mpg": 50, "kWh_per_100km": None, "acceptance_rate": 83,
        "reliability": 90, "average_pay": 13, "capacity_lbs": 28, "available": True
    },
    {
        "id": "d10", "lat": 30.3769, "lon": -97.6851, "vehicle_type": "diesel",
        "mpg": 22, "kWh_per_100km": None, "acceptance_rate": 55,
        "reliability": 70, "average_pay": 17.5, "capacity_lbs": 15, "available": False
    },
]

DELIVERIES = [
    {
        "id": "order_001",
        "pickup_lat": WALMART_STORE["pickup_lat"],
        "pickup_lon": WALMART_STORE["pickup_lon"],
        "drop_lat": 30.3475,
        "drop_lon": -97.6951,
        "size_lbs": 15,
        "traffic_delay_min": 4,
        "weather_delay_factor": 0.1
    },
    {
        "id": "order_002",
        "pickup_lat": WALMART_STORE["pickup_lat"],
        "pickup_lon": WALMART_STORE["pickup_lon"],
        "drop_lat": 30.3801,
        "drop_lon": -97.7251,
        "size_lbs": 40,
        "traffic_delay_min": 10,
        "weather_delay_factor": 0.3
    },
    {
        "id": "order_003",
        "pickup_lat": WALMART_STORE["pickup_lat"],
        "pickup_lon": WALMART_STORE["pickup_lon"],
        "drop_lat": 30.3444,
        "drop_lon": -97.6871,
        "size_lbs": 8,
        "traffic_delay_min": 2,
        "weather_delay_factor": 0.0
    }
]
