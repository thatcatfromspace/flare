import requests

class TrafficClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://router.hereapi.com/v8/routes"

    def get_traffic_delay_minutes(self, origin_lat, origin_lon, dest_lat, dest_lon):
        try:
            params = {
                "transportMode": "car",
                "origin": f"{origin_lat},{origin_lon}",
                "destination": f"{dest_lat},{dest_lon}",
                "return": "summary",
                "routingMode": "fast",
                "apikey": self.api_key,
            }

            response = requests.get(self.base_url, params=params)
            data = response.json()
            summary = data["routes"][0]["sections"][0]["summary"]

            duration_with_traffic = summary["duration"] / 60  # in minutes
            base_duration = summary["baseDuration"] / 60  # in minutes
            delay = max(duration_with_traffic - base_duration, 0)

            return round(delay, 2)

        except Exception as e:
            print(f"[HERE Traffic API Error]: {e}")
            return 5  # default 5-min delay if API fails
