import requests

class WeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_delay_map = {
            "Thunderstorm": 0.6,
            "Drizzle": 0.2,
            "Rain": 0.3,
            "Snow": 0.4,
            "Clear": 0.0,
            "Clouds": 0.1,
            "Mist": 0.2,
            "Haze": 0.2,
            "Fog": 0.3,
            "Tornado": 0.9,
        }
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_delay_factor(self, lat, lon):
        try:
            url = "https://api.openweathermap.org/data/3.0/onecall"
            params = {
                "lat": lat,
                "lon": lon,
                "exclude": "minutely,hourly,daily,alerts",
                "appid": self.api_key,
                "units": "imperial"
            }
            response = requests.get(url, params=params, timeout=3)
            data = response.json()

            if "current" in data and "weather" in data["current"]:
                condition = data["current"]["weather"][0]["main"]

                print(f"[Weather Client]: Current weather condition: {condition}")

                return self.weather_delay_map.get(condition, 0.1)  # default fallback
            
            
            else:
                print("[Weather Client]: Unexpected response structure.")
                return 0.1

        except Exception as e:
            print(f"[Weather Client Error]: {e}")
            return 0.1  # fail-safe default delay
