import hashlib
import psycopg2
from dotenv import load_dotenv
from database import cursor, connection
from utils import *
import pwinput
import email_validator


class User: 
    def __init__(self, user_id, first_name, last_name, email) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        print(f"Hello, {first_name} {last_name}")

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
        password = pwinput.pwinput("Enter your password (1 to return, 2 to exit): ")
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

valid_data = []
      
def validate_first_name(first_name, valid_data):
    """
    Validates a first name and updates a list of valid inputs.

    Args:
        first_name (str): The first name to validate.
        valid_data (list): The list to update with valid inputs.

    Returns:
        bool: True if the first name is valid, False otherwise.
    """

    while True:
        if first_name == "1" or first_name == "2":
            return check_return_exit(first_name)

        if not first_name.isalpha():
            print("First name must contain only letters.")
            first_name = input("Enter your first name (1 to return, 2 to exit): ")
            continue

        if len(first_name) < 2 or len(first_name) > 50:
            print("First name cannot be longer than 50 characters.")
            first_name = input("Enter your first name (1 to return, 2 to exit): ")
            continue
        
        valid_data.append(first_name)
        return True

def validate_last_name(last_name, valid_data):
    """
    Validates a last name and updates a list of valid inputs.

    Args:
        last_name (str): The last name to validate.
        valid_data (list): The list to update with valid inputs.

    Returns:
        bool: True if the last name is valid, False otherwise.
    """

    while True:
        if last_name == "1" or last_name == "2":
            return check_return_exit(last_name)
        
        if not last_name.isalpha():
            print("Last name must contain only letters.")
            last_name = input("Enter your last name (1 to return, 2 to exit): ")
            continue

        if len(last_name) < 2 or len(last_name) > 100:
            print("Last name cannot be longer than 100 characters.")
            last_name = input("Enter your last name (1 to return, 2 to exit): ")
            continue
        
        valid_data.append(last_name)
        return True

def validate_email_unique(email, valid_data):
    """
    Validates an email address for uniqueness and length, and updates a list of valid inputs.

    Args:
        email (str): The email address to validate.
        valid_data (list): The list to update with valid inputs.

    Returns:
        bool: True if the email is unique and valid, False otherwise.
    """

    while True:
        if email == "1" or email == "2":
            return check_return_exit(email)

        try:
            # Validate email address using email_validator
            is_valid = email_validator.validate_email(email)

            if not is_valid:
                # Get the specific error message
                error_message = email_validator.get_error_message(email)
                print(f"Invalid email address: {error_message}")
                email = input("Enter your email address (1 to return, 2 to exit): ")
                continue

            # Check if the email exists (using the established connection)
            cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            
            if len(email) > 255:
                print("Email cannot be longer than 255 characters.")
                email = input("Enter your email address (1 to return, 2 to exit): ")
                continue

            if not result:
                valid_data.append(email)
                return True
            else:
                print("Email already exists.")
                email = input("Enter your email address (1 to return, 2 to exit): ")
                continue
        except Exception as e:
            print(f"Error: {e}")
            email = input("Enter your email address (1 to return, 2 to exit): ")
            continue

def validate_username(username, valid_data):
    """
    Validates a username, ensuring it contains only alphanumeric characters, is within the specified length, and is unique in the database.

    Args:
        username (str): The username to validate.
        valid_data (list): The list to update with valid inputs.

    Returns:
        bool: True if the username is valid, False otherwise.
    """

    while True:
        if username == "1" or username == "2":
            return check_return_exit(username)
        
        try:
            if not username.isalnum() or len(username) < 3 or len(username) > 12:
                print("Username must contain only letters and numbers, and be between 3 and 12 characters long.")
                username = input("Enter your username (1 to return, 2 to exit): ")
                return validate_username(username, valid_data)

            # Check if the username exists (using the established connection)
            cursor.execute("SELECT 1 FROM users WHERE user_name = %s", (username,))
            result = cursor.fetchone()

            if result:
                print("Username already exists. Please choose a different username.")
                username = input("Enter your username (1 to return, 2 to exit): ")
                return validate_username(username, valid_data)

            valid_data.append(username)
            return True
        except Exception as e:
            print(f"Error: {e}")
            username = input("Enter your username (1 to return, 2 to exit): ")
            continue

def validate_password(password, valid_data):
    """
    Validates a password, ensuring it is at least 12 characters long, and hashes it.

    Args:
        password (str): The password to validate.
        valid_data (list): The list to update with valid inputs.

    Returns:
        bool: True if the password is valid, False otherwise.
    """

    while True:
        if password == "1" or password == "2":
            return check_return_exit(password)
        
        if len(password) < 12:
            print("Password must be at least 12 characters long.")
            password = pwinput.pwinput("Enter your password (1 to return, 2 to exit): ")
            continue
        
        # Hash the password
        password_hash = hashlib.sha3_224()
        password_hash.update(password.encode())
        hashed_password = password_hash.hexdigest()
        
        valid_data.append(hashed_password)
        return True

def registration_function():
    '''This function registers a new user and if successful goes back to the authentication menu'''
    
    first_name = input("Enter your first name (1 to return, 2 to exit): ")
    if validate_first_name(first_name, valid_data):
        
        last_name = input("Enter your last name (1 to return, 2 to exit): ")
        if validate_last_name(last_name, valid_data):
            
            username = input("Enter your username (1 to return, 2 to exit): ") 
            if validate_username(username, valid_data):
                
                password = pwinput.pwinput("Enter your password (1 to return, 2 to exit): ") 
                if validate_password(password, valid_data):
                    
                    email = input("Enter your email address (1 to return, 2 to exit): ")
                    if validate_email_unique(email, valid_data):
                        # USE ONLY VALIDATED DATA!
                        register_new_user(valid_data[0], valid_data[1], valid_data[2], valid_data[3], valid_data[4])        
            
    authentication_menu()

    
def register_new_user(first_name, last_name, username, password, email):
    '''This function adds a new user to the database'''
    try:
        query = f'''INSERT INTO users (first_name, last_name, email, user_name, password)                
        VALUES ('{first_name}', '{last_name}', '{email}', '{username}', '{password}')'''    
        cursor.execute(query)
        connection.commit()  
        print(f"Congratulations, {first_name}! You have been registered successfully!\n") 
    except psycopg2.Error as e:
        print(f"Database error: {e}")

def authentication_menu(): 
    '''This function gets user's choice of action and runs
    corresponding fuction'''
    user_options = {'1':'Log in', '2':'Register', '3':'Exit'}
    choice = menu_user_options(user_options)
    if choice == "1": #login
        user = login_function() 
    elif choice == "2": #register
        user = registration_function() 
    elif choice == "3":  # exit
        exit_program() 
    return user

    
  

  
