import psycopg2
from database import cursor, connection
from tabulate import tabulate 
from authentication import User
from utils import *
import datetime
from message import *

class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

class Status:
    def __init__(self, status_id, status_name):
        self.status_id = status_id
        self.status_name = status_name        


def view_tasks(user,option):
    user_id = user.user_id
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
    return(full_data,table)

def view_tasks_send_email(user, option):
    full_data, table = view_tasks(user,option)
    while True:
        email_option = input("Whould you like to get your tasks by email?\n1: yes\n2: no\nEnter your choice: ")
        if email_option == '1':
            send_email(table)
            print("Check your email!")
            break
        else:
            print('Invalid input. Try again')
    return full_data


def check_return_exit(choice):
    '''Checks if the user's choice was to return or to exit'''
    if choice == "1":
        tasks_menu()
    elif choice == "2":
        exit_program()
    else:
        return True

def add_new_task_to_db(user,task):
    '''This function adds a new task to the database'''
    user_id = user.user_id
    try:
        query = f'''INSERT INTO tasks (user_id, date_start, date_finish, status_id, category_id, task_content, task_comment)	
    VALUES		
    ({user_id}, '{task['date_start']}', '{task['date_finish']}', {task['status']}, {task['category']}, '{task['content']}', '{task['comment']}')		
		'''	
        cursor.execute(query)
        connection.commit()  
        print(f"Your task was added successfully!\n") 
    except psycopg2.Error as e:
        print(f"Database error: {e}") 

def create_task(user):
    while True:
        task = {}
        
        # Category Selection
        print("\nCategory: ")
        category = choose_category_or_status('category')
        task['category'] = category.category_id
        
         # Validate Category
        if not (1 <= task['category'] <= 8):
            print("Category must be an integer value within the range 1-8.")
            continue
        
        # Task Content
        while True:
            task['content'] = input('Please write down your task: ')
            if task['content'].strip() == "":
                print("Task content cannot be empty.")
            elif len(task['content']) > 255:
                print("Task content cannot be longer than 255 characters.")
            else:
                break
            
        # Status Selection
        print("\nStatus: ")
        status = choose_category_or_status('status')
        task['status'] = status.status_id
        
        # Validate Status
        if not (1 <= task['status'] <= 4):
            print("Status must be an integer value within the range 1-4.")
            continue
        
        # Deadline
        while True:
            try:
                task['date_finish'] = input("Please enter the deadline in format 'YYYY-MM-DD': ")
                deadline = datetime.datetime.strptime(task['date_finish'], "%Y-%m-%d")
                now = datetime.datetime.today()
                task['date_start'] = now.strftime('%Y-%m-%d')
                
                if deadline.date() >= now.date():
                    break
                else:
                    print("Deadline can't be before today.")
            except ValueError:
                print("Invalid date format. Please use 'YYYY-MM-DD'.")
        
        # Comment        
        task['comment'] = input ('Please enter your comment: ')
        
        # Confirmation
        while True:
            print('\nThis is your task:')
            print(f"Category: {category.category_name}\nContent: {task['content']}\nStatus: {status.status_name}\nDeadline: {task['date_finish']}\nComment: {task['comment']}")
            is_correct = input("Enter 1 if it is correct, 2 if you want to change something: ")
            if is_correct in ['1', '2']:
                if is_correct == '1':
                    add_new_task_to_db(user, task)
                    return
                break
            else:
                print("Invalid input. Please enter 1 to confirm or 2 to change something.")

def delete_task_from_db(task_id):
    query = f"DELETE FROM tasks WHERE task_id ={task_id} "
    try:
        cursor.execute(query)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        exit(1)

def delete_task(user):
    tasks = view_tasks_menu(user)
    while True:
        number = int(input("Enter the number of the task you want to delete: "))
        if number <= len(tasks):
            break
        else:
            print("This is not a  corrent task number. Try again")
    for task in tasks:
        if task['No.'] == number:
            task_id_to_delete = task['task_id']
    delete_task_from_db(task_id_to_delete)
    print("Your task was deleted")

        
def choose_category_or_status(option):
    '''This function displays the choice of categories or statuses and returns user's choice'''
    if option == 'category':
        query = "SELECT * FROM categories"
    else:
        query = "SELECT * FROM statuses"
    
    cursor.execute(query)
    database = cursor.fetchall()
    
    for item in database:
        print(f"{item[0]}. {item[1]}")
    
    while True:
        try:
            choice = int(input("Please choose the number: "))
            if option == 'category' and (choice < 1 or choice > 8):
                print("Category must be an integer value within the range 1-8.")
            elif option == 'status' and (choice < 1 or choice > 4):
                print("Status must be an integer value within the range 1-4.")
            elif choice >= 1 and choice <= len(database):
                break
            else:
                print("This is the wrong number. Try again!")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    for item in database:
        if item[0] == choice:
            if option == 'category':
                result = Category(item[0], item[1])
            else:
                result = Status(item[0], item[1])
    
    return result

def view_tasks_menu(user):
    '''This function gets user's choice of action in view meny and runs corresponding fuction'''
    user_options = {'1':'View all', '2':'View by category', '3': 'View by status', '4':'Return to task menu', '5':'Exit'}
    choice = menu_user_options(user_options)
    if choice == "1": # View all
        tasks = view_tasks_send_email(user, "all")
    elif choice == "2": #View by category
        print("\nCategories: ")
        category = choose_category_or_status('category')
        tasks = view_tasks_send_email(user, category)
    elif choice == "3": # View by status
        print("\nStatuses: ")
        status = choose_category_or_status('status')
        tasks = view_tasks_send_email(user, status)
    elif choice == "4": # Return to task menu
        tasks_menu(user)
    else: # choice == "5" Exit
        exit_program() 
    return tasks


# def tasks_menu(user): 
def tasks_menu(user): 
    '''This function gets user's choice of action in tasks menu and runs
    corresponding fuction'''
    user_options = {'1':'View tasks', '2':'Create new tasks','3':'Delete tasks', '4':'Exit'}
    choice = menu_user_options(user_options)
    if choice == "1": # View Tasks
        view_tasks_menu(user)
        tasks_menu(user)
    elif choice == "2": #Create new task
        create_task(user)
        tasks_menu(user)
    elif choice == "3": # Delete tasks
        delete_task(user)
        tasks_menu(user)
    else: # choice == "5" exit
        exit_program() 
