from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    #bu using property decortaor we can use this function name as key, like settings.POSTGRES_URL
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = DatabaseSettings()
print("keys :: ",settings.POSTGRES_DB)
print("keys :: ",settings.POSTGRES_HOST)
print("keys :: ",settings.POSTGRES_USER)
print("keys :: ",settings.POSTGRES_URL)
