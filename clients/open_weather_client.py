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
            params = {"lat": lat, "lon": lon, "appid": self.api_key}
            response = requests.get(self.base_url, params=params)
            data = response.json()

            condition = data["weather"][0]["main"]
            return self.weather_delay_map.get(condition, 0.1)  # default to light delay

        except Exception as e:
            print(f"[Weather API Error]: {e}")
            return 0.1  # fallback if API fails


    
