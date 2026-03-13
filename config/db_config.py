import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

class Db_config:

    def __init__(self) -> None:
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")


    def get_db_connection(self):
        conn = psycopg.connect(f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return conn
    