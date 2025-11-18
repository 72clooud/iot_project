from pydantic import BaseModel, Field
from datetime import datetime

class TelemetryModel(BaseModel):
    location: str
    country: str
    lon: float
    lat: float
    aqi: int
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float = Field(..., alias="pm2_5")
    pm10: float
    nh3: float
    uv_index: float
    time: datetime
    