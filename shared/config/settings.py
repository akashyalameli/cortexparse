from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    API_HOST: str
    API_PORT: int

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str

    OLLAMA_BASE_URL: str

    MAX_RETRIES: int
    CONFIDENCE_THRESHOLD: float

    class Config:
        env_file = ".env"


settings = Settings()
