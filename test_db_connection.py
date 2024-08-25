import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

# Connect to PostgreSQL database
try:
    connection = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
except psycopg2.Error as e:
    print(f"Error connecting to database: {e}")
    exit(1)

cursor = connection.cursor()

# Execute a query to test the connection
cursor.execute("""
    DELETE FROM tasks
    WHERE 
    date_finish IS NULL OR 
    task_id IS NULL OR
    user_id IS NULL OR
    date_start IS NULL OR
    user_id IS NULL OR
    status_id IS NULL OR
    category_id IS NULL OR
    task_content IS NULL OR
    task_comment IS NULL;
""")

connection.commit()

# Close the connection
cursor.close()
connection.close()