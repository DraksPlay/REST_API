import os
from dotenv import load_dotenv


load_dotenv()


DEBUG = True

# Database
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL_PROD = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@db:{DB_PORT}/{DB_NAME}"