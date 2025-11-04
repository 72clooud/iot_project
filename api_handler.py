from dotenv import load_dotenv
from pyowm import OWM

from datetime import datetime, timezone
import os

load_dotenv()

class ApiHandler:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.mgr_air = OWM(self.api_key).airpollution_manager()
        self.mgr_uv = OWM(self.api_key).uvindex_manager()
        self.mgr_location = OWM(self.api_key).geocoding_manager()
        self.time_fileds = ['reception_time', 'reference_time']

    def _convert_int_to_date(self, value: str, dictionary: dict) -> None:
            dictionary[value] = datetime.fromtimestamp(
                dictionary[value], tz=timezone.utc
            ).strftime('%Y-%m-%d %H:%M:%S UTC')

    def fetch_air_status(self, lat: float, lon: float, enable_location: bool = False) -> dict:
        air_status = self.mgr_air.air_quality_at_coords(lat, lon).to_dict()
        
        for time_filed in self.time_fileds:
            self._convert_int_to_date(time_filed, air_status)
        
        if enable_location:
            location = self.mgr_location.reverse_geocode(lat=lat, lon=lon)
            location_name = location[0].name
            air_status['location']['name'] = location_name

        return air_status

    def fetch_uv_index(self, lat: float, lon: float, enable_location: bool = False) -> dict:
        uv_index = self.mgr_uv.uvindex_around_coords(lat, lon).to_dict()

        for time_filed in self.time_fileds:
            self._convert_int_to_date(time_filed, uv_index)

        if enable_location:
            location = self.mgr_location.reverse_geocode(lat=lat, lon=lon)
            location_name = location[0].name
            uv_index['location']['name'] = location_name

        return uv_index


    def get_all_data(self, lat: float, lon: float, enable_location: bool = False) -> dict:
        air_status: dict = self.fetch_air_status(lat, lon, enable_location)
        uv_index: dict = self.fetch_uv_index(lat, lon, enable_location)

        air_quality_data = air_status.get('air_quality_data', {})
        location_data = air_status.get('location', {})


        final_payload = {
            'reference_time': air_status['reference_time'],
            'location_name': air_status['location']['name'],
            'location_country': air_status['location']['country'],
            'lat': location_data['coordinates']['lat'],
            'lon': location_data['coordinates']['lon'],
            'reception_time': air_status['reception_time'],
            **air_quality_data,
            'uv_index': uv_index['value']
        }

        return final_payload


