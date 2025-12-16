from api_handler import ApiHandler
from azure_sender import AzureIotHubSender
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("uamqp").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
    api_handler_instance = ApiHandler()
    azure_sender_instance = AzureIotHubSender()

    path = "../data/polish_cities_spatially_selected.parquet"
    df = pd.read_parquet(path)
    
    for index, row in df.iterrows():
        lat = row['Lat']
        lon = row['Lon']
        city = row['City']

        try:
            data = api_handler_instance.get_all_data(lat, lon, city, "PL")
            logging.info(f"Fetched data for {city} (Lat: {lat}, Lon: {lon})")
            try:
                azure_sender_instance.send_telemetry_message(data)
                logging.info(f"Sent data for {city} (Lat: {lat}, Lon: {lon}), {index + 1}/{len(df)}")
            except Exception as e:
                logging.error(f"Error sending data for {city} (Lat: {lat}, Lon: {lon}): {e}")
        except Exception as e:
            logging.error(f"Error fetching data for {city} (Lat: {lat}, Lon: {lon}): {e}")
            continue

if __name__ == "__main__":
    main()