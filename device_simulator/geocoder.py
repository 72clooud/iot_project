import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os

class GeoDataFetch:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="iot_simulator_project_pl_v1")
        self.output_path = "../data/polish_cities_with_coordinates.parquet"

    def add_coordinates(self, input_path: str):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"The file {input_path} does not exist.")
        
        df = pd.read_parquet(input_path)

        df['Lat'] = None
        df['Lon'] = None

        for index, row in df.iterrows():
            city = row['Miasto']

            try:
                location = self.geolocator.geocode(city, timeout=10)

                if location:
                    df.at[index, 'Lat'] = location.latitude
                    df.at[index, 'Lon'] = location.longitude
                    print(f"Found coordinates for {city}: ({location.latitude}, {location.longitude})")
                else:
                    print(f"Could not find coordinates for {city}")

            except GeocoderTimedOut:
                print(f'Erorr for {city}')

            time.sleep(1.1)
        df.to_parquet(self.output_path, index=False)

if __name__ == "__main__":
    geofetcher = GeoDataFetch()
    geofetcher.add_coordinates("../data/polish_cities.parquet")


