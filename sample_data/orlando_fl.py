WALMART_STORE = {
    "id": "store_orlando_001",
    "name": "Walmart Supercenter - Orlando FL",
    "pickup_lat": 28.5383,
    "pickup_lon": -81.3792
}

DRIVERS = [
    {
        "id": "d1", "lat": 28.5401, "lon": -81.3851, "vehicle_type": "electric",
        "mpg": None, "kWh_per_100km": 14, "acceptance_rate": 80,
        "reliability": 85, "average_pay": 15, "capacity_lbs": 25, "available": True
    },
    {
        "id": "d2", "lat": 28.5365, "lon": -81.3750, "vehicle_type": "petrol",
        "mpg": 30, "kWh_per_100km": None, "acceptance_rate": 85,
        "reliability": 91, "average_pay": 13, "capacity_lbs": 30, "available": True
    },
    {
        "id": "d3", "lat": 28.5392, "lon": -81.3721, "vehicle_type": "hybrid",
        "mpg": 48, "kWh_per_100km": None, "acceptance_rate": 75,
        "reliability": 80, "average_pay": 14, "capacity_lbs": 20, "available": True
    },
    {
        "id": "d4", "lat": 28.5410, "lon": -81.3900, "vehicle_type": "diesel",
        "mpg": 22, "kWh_per_100km": None, "acceptance_rate": 90,
        "reliability": 78, "average_pay": 16, "capacity_lbs": 45, "available": True
    },
    {
        "id": "d5", "lat": 28.5450, "lon": -81.3790, "vehicle_type": "petrol",
        "mpg": 28, "kWh_per_100km": None, "acceptance_rate": 60,
        "reliability": 70, "average_pay": 17, "capacity_lbs": 15, "available": True
    },
    {
        "id": "d6", "lat": 28.5330, "lon": -81.3820, "vehicle_type": "electric",
        "mpg": None, "kWh_per_100km": 16, "acceptance_rate": 92,
        "reliability": 95, "average_pay": 12, "capacity_lbs": 35, "available": False
    },
    {
        "id": "d7", "lat": 28.5370, "lon": -81.3870, "vehicle_type": "petrol",
        "mpg": 32, "kWh_per_100km": None, "acceptance_rate": 88,
        "reliability": 88, "average_pay": 13.5, "capacity_lbs": 30, "available": True
    },
    {
        "id": "d8", "lat": 28.5305, "lon": -81.3795, "vehicle_type": "electric",
        "mpg": None, "kWh_per_100km": 18, "acceptance_rate": 70,
        "reliability": 60, "average_pay": 14.5, "capacity_lbs": 40, "available": True
    },
    {
        "id": "d9", "lat": 28.5435, "lon": -81.3720, "vehicle_type": "diesel",
        "mpg": 20, "kWh_per_100km": None, "acceptance_rate": 65,
        "reliability": 82, "average_pay": 15.5, "capacity_lbs": 50, "available": True
    },
    {
        "id": "d10", "lat": 28.5352, "lon": -81.3699, "vehicle_type": "hybrid",
        "mpg": 50, "kWh_per_100km": None, "acceptance_rate": 95,
        "reliability": 97, "average_pay": 12.8, "capacity_lbs": 28, "available": True
    },
]

DELIVERIES = [
    {
        "id": "order_100",
        "pickup_lat": WALMART_STORE["pickup_lat"],
        "pickup_lon": WALMART_STORE["pickup_lon"],
        "drop_lat": 28.5411,
        "drop_lon": -81.3888,
        "size_lbs": 10,  # Easy, almost all drivers qualify
    },
    {
        "id": "order_101",
        "pickup_lat": WALMART_STORE["pickup_lat"],
        "pickup_lon": WALMART_STORE["pickup_lon"],
        "drop_lat": 28.5499,
        "drop_lon": -81.3955,
        "size_lbs": 38,  # High capacity test
    },
    {
        "id": "order_102",
        "pickup_lat": WALMART_STORE["pickup_lat"],
        "pickup_lon": WALMART_STORE["pickup_lon"],
        "drop_lat": 28.5271,
        "drop_lon": -81.3681,
        "size_lbs": 22,  # Just enough edge for filtering
    }
]
