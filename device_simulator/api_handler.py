from dotenv import load_dotenv
from datetime import datetime, timezone
import os
import requests

load_dotenv()

class ApiHandler:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.air_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.uv_url = "https://api.openweathermap.org/data/2.5/uvi"
        self.geo_url = "http://api.openweathermap.org/geo/1.0/reverse"
        path = "../data/polish_cities_with_coordinates.parquet"
        self.cities_path = path if os.path.exists(path) else None

    def _convert_int_to_date(self, value: str, dictionary: dict) -> None:
            dictionary[value] = datetime.fromtimestamp(
                dictionary[value], tz=timezone.utc
            ).strftime('%Y-%m-%d %H:%M:%S UTC')

    def fetch_location(self, lat: float, lon: float):
        params = {"lat": lat, "lon": lon, "appid": self.api_key}
        response = requests.get(self.geo_url, params=params)

        if response.status_code != 200:
            raise RuntimeError(f'API Error: {response.status_code} - {response.text}')

        geo_data = response.json()[0]

        return geo_data

    def fetch_air_status(self, lat: float, lon: float, location: str, country: str) -> dict:
        params = {"lat": lat, "lon": lon, "appid": self.api_key}
        response = requests.get(self.air_url, params=params)

        if response.status_code != 200:
            raise RuntimeError(f'API Error: {response.status_code} - {response.text}')

        data = response.json()

        entry = data['list'][0]
        air_quality_data = entry['components']

        self._convert_int_to_date('dt', entry)

        final_payload = {
            'location': location,
            'country': country,
            'lon': data['coord']['lon'],
            'lat': data['coord']['lat'],
            'aqi': entry['main']['aqi'],
            **air_quality_data,
            'time': entry['dt'],
            'coordinates_geojson': {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }

        return final_payload


    def fetch_uv_index(self, lat: float, lon: float, location: str, country: str) -> dict:
        params = {"lat": lat, "lon": lon, "appid": self.api_key}
        response = requests.get(self.uv_url, params=params)

        if response.status_code != 200:
            raise RuntimeError(f'API Error: {response.status_code} - {response.text}')

        data = response.json()
        self._convert_int_to_date('date', data)

        final_payload = {
            'location': location,
            'country': country,
            'lon': data['lon'],
            'lat': data['lat'],
            'value': data['value'],
            'time': data['date'],
            'coordinates_geojson': {
                "type": "Point",
                "coordinates": [lon, lat]
            } 
        }

        return final_payload


    def get_all_data(self, lat: float, lon: float, location: str, country: str) -> dict:
        air_status: dict = self.fetch_air_status(lat, lon, location, country)
        uv_index: dict = self.fetch_uv_index(lat, lon, location, country)

        final_payload = {
            'location': location,
            'country': country,
            'lon': air_status['lon'],
            'lat': air_status['lat'],
            'aqi': air_status['aqi'],
            "co": air_status['co'],
            "no": air_status['no'],
            "no2": air_status['no2'],
            "o3": air_status['o3'],
            "so2": air_status['so2'],
            "pm2_5": air_status['pm2_5'],
            "pm10": air_status['pm10'],
            "nh3": air_status['nh3'],
            'uv_index': uv_index['value'],
            'time': air_status['time'],
            'coordinates_geojson': {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }

        return final_payload
