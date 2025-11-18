from pydantic import BaseModel, Field, ConfigDict

class CoordinatesGeoJSON(BaseModel):
    type: str = "Point"
    coordinates: list[float]

class TelemetryModel(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        from_attributes=True
    )
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
    time: str
    coordinates_geojson: CoordinatesGeoJSON