from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    cosmosdb_database: str
    cosmosdb_container: str
    azure_cosmosdb_connection_string: str

    class Config:
        env_file = ".env"