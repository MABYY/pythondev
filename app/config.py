from pydantic import BaseSettings
## pydentic model to validate the environmental variables

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env" # --> indicates where to find the env variables


settings = Settings() # create instance of the Settings class
