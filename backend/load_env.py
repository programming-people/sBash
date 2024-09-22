import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

IMG_PATH = os.getenv("IMG_PATH")

if not DB_HOST or not DB_USER or not DB_NAME or not DB_PASS or not IMG_PATH:
    raise Exception("environment variables are required")
