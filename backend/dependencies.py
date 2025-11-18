import numpy as np
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from azure.core.exceptions import ResourceNotFoundError

load_dotenv()

class AzureCosmosdbHandler:
    def __init__(self, db: str, container: str, conn_str: str):
        try:
            self.cosmosdb_client = CosmosClient.from_connection_string(conn_str=conn_str)
            self.db = self.cosmosdb_client.get_database_client(database=db)
            self.container = self.db.get_container_client(container=container)
            print(f'Succesful connect to container: {container}')
        except Exception as e:
            print(f'Error: {e}') 

    def get_file(self, lat: float, lon: float):
        query = """
            SELECT TOP 1 c FROM c 
            ORDER BY ST_DISTANCE(c.coordinates_geojson, {'type': 'Point', 'coordinates': [@lon, @lat]}) ASC
        """

        params = [
            {"name": "@lat", "value": lat},
            {"name": "@lon", "value": lon}
        ]

        items = list(self.container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

        if not items:
            raise ResourceNotFoundError(f"No item found for lat={lat}, lon={lon}")

        full_document = items[0]['c']
        return full_document['Body']
    