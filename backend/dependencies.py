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
            SELECT TOP 1 * FROM c 
            ORDER BY ST_DISTANCE(c.Body.coordinates_geojson, @point) ASC
        """

        point_object = {
            "type": "Point",
            "coordinates": [lon, lat]
        }

        params = [
            {"name": "@point", "value": point_object}
        ]

        items = list(self.container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

        if not items:
            print(f"Warning: No items found near {lat}, {lon}")
            raise ResourceNotFoundError(f"No item found for lat={lat}, lon={lon}")

        full_document = items[0]

        return full_document.get('Body', full_document)