from dotenv import load_dotenv
import os

load_dotenv()

pg_url = os.getenv("POSTGRES_URL")
