import sys
import hashlib
import psycopg2
from dotenv import load_dotenv
import os
from database import cursor, connection

class User: 
    def __init__(self, user_id, first_name, last_name, email) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        print(f"Hello, {first_name} {last_name}")

# THIS SHOULD BE IN A DIFFERENT MODULE
def exit_program(): 
    '''Exits the program and closes connection to database'''
    print("\nI hoped you enjoyed using this app. See you next time!") 
    connection.close()
    cursor.close()
    sys.exit() 

def check_return_exit(choice):
    '''Checks if the user's choice was to return or to exit'''
    if choice == "1":
        authentication_menu()
    elif choice == "2":
        exit_program()
    else:
        return True

def login_function():
    '''This function check username - password combination and if successful returns and object of User'''
    username = input("Enter your username (1 to return, 2 to exit): ") 
    if check_return_exit(username):
        password = input("Enter your password (1 to return, 2 to exit): ")
        if check_return_exit(password):
            try:
                password_hash = hashlib.sha3_224()
                password_hash.update(str(password).encode())
                query = f'''SELECT user_id, first_name, last_name, email FROM users
                WHERE user_name = '{username}' AND password = '{password_hash.hexdigest()}';'''
                cursor.execute(query)
                result = cursor.fetchone() 
                connection.commit()  
            except psycopg2.Error as e:
                print(f"Database error: {e}") 
            if result is not None:
                user = User(result[0], result[1], result[2], result[3])
    return user            
        

# def validate_email_unique(email): 
# # ... (function definition here)

# def validate_username(username): 
# # ... (function definition here) 

# def validate_password(password): 
# # ... (function definition here)


def register_new_user(first_name, last_name, username, password, email):
    '''This function adds a new user to the database'''
    try:
        password_hash = hashlib.sha3_224()
        password_hash.update(str(password).encode())
        query = f'''INSERT INTO users (first_name, last_name, email, user_name, password)				
        VALUES ('{first_name}', '{last_name}', '{email}', '{username}', '{password_hash.hexdigest()}')'''	
        cursor.execute(query)
        connection.commit()   
    except psycopg2.Error as e:
        print(f"Database error: {e}") 
    
def registration_function():
    '''This fuction registers a new user andif successfull gors back to authontication menu'''
    first_name = input("Enter your first name (1 to return, 2 to exit): ")
    if check_return_exit(first_name):
        last_name = input("Enter your last name (1 to return, 2 to exit): ")
        if check_return_exit(last_name):
            username = input("Enter your username (1 to return, 2 to exit): ") 
            if check_return_exit(username):
                password = input("Enter your password (1 to return, 2 to exit): ") 
                if check_return_exit(password):
                    email = input("Enter your email address (1 to return, 2 to exit): ")
                    if check_return_exit(email):
                        pass
                        # VALIDATION OF ALL THE DATA
                        # if validate_email_unique(email) and ...

                        register_new_user(first_name, last_name, username, password, email)
                        print(f"Congratulations, {first_name}! You have been registered successfully!")
    authentication_menu()


def authentication_menu_input():
    '''This function displays authentification menu.
    It asks the user to choose an action (log in, register, exit)
    and runs until the accepted awnser is given. It returns
    user's choice of action '''
    choice = ''
    accepted_choiced = ['1', '2', '3']
    while choice not in accepted_choiced:
        print("What would you like to do?:\n1. Log in\n2. Register\n3. Exit") 
        choice = input("Enter your choice (1-3): ") 
        if choice in accepted_choiced:
            return choice
        else:
            print("\nInvalid choice. Please try again.") 

def authentication_menu(): 
    '''This function gets user's choice of action and runs
    corresponding fuction'''

    choice = authentication_menu_input()
    if choice == "1": #login
        user = login_function() 
    elif choice == "2": #register
        user = registration_function() 
    elif choice == "3":  # exit
        exit_program() 
    return user

    
  

  
