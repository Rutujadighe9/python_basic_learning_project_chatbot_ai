import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set in the environment or .env file")
        self.DATABASE_URL = database_url

        jwt_secret_key = os.getenv("JWT_SECRET_KEY")
        if not jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY is not set in the environment or .env file")
        self.JWT_SECRET_KEY = jwt_secret_key


settings = Settings()
