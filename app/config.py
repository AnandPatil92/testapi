from pydantic import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = "testapi"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    port: int = 0000


class DatabaseSettings(BaseSettings):
    DB_URL = str
    DB_Name = str

class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
