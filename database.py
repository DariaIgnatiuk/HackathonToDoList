import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

connection = psycopg2.connect(database = DB_NAME,
                             user = DB_USER,
                             password = DB_PASSWORD,
                             host = DB_HOST,
                             port = DB_PORT)
cursor = connection.cursor()
