
# !make sure we can collect data from db from task_id, the way it would not be printed but we will have it for internal use
# !we take task number from the screen (how) and based on it we ask user to (edit, delete, send to email) - .

# !new code
import os
import psycopg2
from dotenv import load_dotenv
from tabulate import tabulate

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

# Query to join the tables and get the output columns renamed and in specified order
query = """
SELECT task_id,
       ROW_NUMBER() OVER () AS "No.",
       tasks.task_content AS "Task",
       categories.category_name AS "Category",
       statuses.status_name AS "Status",
       tasks.date_start AS "Start Date",
       tasks.date_finish AS "Deadline",
       tasks.task_comment AS "Comment"
FROM tasks
INNER JOIN categories ON tasks.category_id = categories.category_id
INNER JOIN statuses ON tasks.status_id = statuses.status_id
INNER JOIN users ON tasks.user_id = users.user_id;
"""

# Execute the query
try:
    cursor.execute(query)
    data = cursor.fetchall() # *creates a list of tuples from fetched data (does not work well tabulate directly)
except psycopg2.Error as e:
    print(f"Error executing query: {e}")
    exit(1)

# *Get the column names from the cursor description (it is dictionary of column names and vaue types)
column_names = [description[0] for description in cursor.description]

# *Convert the data list of tuples into a list of dictionaries without 0 column
data_dict_sliced = [dict(zip(column_names[1:], row[1:])) for row in data]

# *Convert the data list of tuples into a list of dictionaries
data_dict = [dict(zip(column_names, row)) for row in data]

# *Create a table using tabulate, directly using the dictionaries
table = tabulate(data_dict_sliced, headers="keys", tablefmt="grid")

# Print the table
print(table)

# Access task_ids for later use
task_ids = [row['task_id'] for row in data_dict]

# Close the connection
cursor.close()
connection.close()