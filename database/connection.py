import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            client_encoding='utf8'  # <--- Essa linha resolve o conflito do "ã"
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None