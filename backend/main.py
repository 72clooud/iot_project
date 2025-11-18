import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException
from azure.core.exceptions import ResourceNotFoundError

from config import AppSettings
from dependencies import AzureCosmosdbHandler
from schemas import TelemetryModel

settings = AppSettings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.db_handler = AzureCosmosdbHandler(
            db=settings.cosmosdb_database,
            container=settings.cosmosdb_container,
            conn_str=settings.azure_cosmosdb_connection_string
        )
        yield
    except Exception as e:
        logging.error(f"Failed to initialize Cosmos DB handler: {e}")
        raise e

app = FastAPI(lifespan=lifespan)

def get_db_handler(request: Request) -> AzureCosmosdbHandler:
    return request.app.state.db_handler

@app.get('/')
def read_root():
    return {'status': 'OK'}

@app.get('/telemetry', response_model=TelemetryModel)
def get_telemetry(lat: float, lon: float, db_handler = Depends(get_db_handler)):
    try:
        results = db_handler.get_file(lat=lat, lon=lon)
        return results
    except ResourceNotFoundError:
        logging.warning(f"Telemetry not found for lat={lat}, lon={lon}")
        raise HTTPException(status_code=404, detail="Telemetry not found")
    except Exception as e:
        logging.error(f'Unexpected error in /telemetry: {e}')
        raise HTTPException(status_code=500, detail=str(e))
