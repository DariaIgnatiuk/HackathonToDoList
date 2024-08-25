import psycopg2
from database import cursor, connection
from tabulate import tabulate 
from authentication import User
from utils import *
import datetime

class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

class Status:
    def __init__(self, status_id, status_name):
        self.status_id = status_id
        self.status_name = status_name        


def view_tasks(option):
    user_id = 14
    if option == "all":
        print("These are all your tasks:")
        query = f""" 
    SELECT
    tasks.task_id,
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
    WHERE tasks.user_id = '{user_id}' 
    """ 
    elif  isinstance(option, Category):
        print(f"These are all your tasks in category {option}:")
        query = f""" 
    SELECT
    tasks.task_id,
    ROW_NUMBER() OVER () AS "No.",
    tasks.task_content AS "Task",
    categories.category_name AS "Category",
    tasks.date_start AS "Start Date",
    tasks.date_finish AS "Deadline",
    tasks.task_comment AS "Comment"
    FROM tasks
    INNER JOIN categories ON tasks.category_id = categories.category_id
    INNER JOIN statuses ON tasks.status_id = statuses.status_id
    WHERE tasks.user_id = '{user_id}' AND  categories.category_name = '{option.category_name}'
    """ 
    elif isinstance(option, Status):
        print(f"These are all your tasks with status {option}:")
        query = f""" 
    SELECT
    tasks.task_id,
    ROW_NUMBER() OVER () AS "No.",
    tasks.task_content AS "Task",
    categories.category_name AS "Category",
    tasks.date_start AS "Start Date",
    tasks.date_finish AS "Deadline",
    tasks.task_comment AS "Comment"
    FROM tasks
    INNER JOIN categories ON tasks.category_id = categories.category_id
    INNER JOIN statuses ON tasks.status_id = statuses.status_id
    WHERE tasks.user_id = '{user_id}' AND  statuses.status_name= '{option.status_name}'
    """  
    try:
        cursor.execute(query)
        data = cursor.fetchall() # *creates a list of tuples from fetched data (does not work well tabulate directly)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        exit(1)

    # *Get the column names from the cursor description (it is dictionary of column names and vaue types)
    column_names = [description[0] for description in cursor.description]

# *Convert the data list of tuples into a list of dictionaries without 0 column
    data_dict = [dict(zip(column_names[1:], row[1:])) for row in data]

# *Convert the data list of tuples into a list of dictionaries
    full_data = [dict(zip(column_names, row)) for row in data]

# *Create a table using tabulate, directly using the dictionaries
    table = tabulate(data_dict, headers="keys", tablefmt="grid")

# Print the table
    print(table) 


def choose_category_or_status(option):
    '''This fuction displays the choice of categories of statuses and returns user's choice'''
    if option == 'category':
        query = "SELECT * FROM categories"
        print("Categories: ")
    else:
        query = "SELECT * FROM statuses"
        print("Statuses: ")
    cursor.execute(query)
    database = cursor.fetchall()
    for item in database:
        print(f"{item[0]}. {item[1]}")
    while True:     
        choice = int(input("Please choose the number: "))
        if choice >= 1 and choice <= len(database):
            break
        print("This is the wrong number. Try again!")          
    for item in database:
        if item[0] == choice:
            if option == 'category':
                result = Category(item[0], item[1])
            else:
                result = Status(item[0], item[1])
    return result


def view_tasks_menu():
    '''This function gets user's choice of action in view meny and runs corresponding fuction'''
    user_options = {'1':'View all', '2':'View by category', '3': 'View by status', '4':'Return to task menu', '5':'Exit'}
    choice = menu_user_options(user_options)
    if choice == "1": # View all
        view_tasks("all")
    elif choice == "2": #View by category
        category = choose_category_or_status('category')
        view_tasks(category)
    elif choice == "3": # View by status
        status = choose_category_or_status('status')
        view_tasks(status)
    elif choice == "4": # Return to task menu
        tasks_menu()
    else: # choice == "5" Exit
        exit_program() 


# def tasks_menu(user): 
def tasks_menu(): 
    '''This function gets user's choice of action in tasks menu and runs
    corresponding fuction'''
    user_options = {'1':'View tasks', '2':'Create new tasks', '3': 'Edit tasks', '4':'Delete tasks', '5':'Exit'}
    choice = menu_user_options(user_options)
    if choice == "1": # View Tasks
        view_tasks_menu()
    elif choice == "2": #Create new task
        pass
    elif choice == "3": # Edit tasks
        pass
    elif choice == "4": # Delete tasks
        pass     
    else: # choice == "5" exit
        exit_program() 

