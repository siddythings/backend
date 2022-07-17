from os import environ
from dotenv import load_dotenv

load_dotenv()

DEBUG = environ.get("DEBUG", False)

SECRET_KEY = environ.get("SECRET_KEY", "secret")


# Database
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", "5432")
DB_NAME = environ.get("DB_NAME", "parking")
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "postgres")

# Tesseract
TESSERACT_PATH = environ.get("TESSERACT_PATH")
