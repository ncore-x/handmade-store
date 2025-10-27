from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SUPERADMIN_PASSWORD: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def JWT_PRIVATE_KEY(self):
        try:
            with open(self.JWT_PRIVATE_KEY_PATH, "r") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise Exception(
                f"Приватный ключ не найден: {self.JWT_PRIVATE_KEY_PATH}")

    @property
    def JWT_PUBLIC_KEY(self):
        try:
            with open(self.JWT_PUBLIC_KEY_PATH, "r") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise Exception(
                f"Публичный ключ не найден: {self.JWT_PUBLIC_KEY_PATH}")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
