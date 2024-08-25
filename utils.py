
from database import cursor, connection
import sys

def exit_program(): 
    '''Exits the program and closes connection to database'''
    print("\nI hope you enjoyed using this app. See you next time!") 
    connection.close()
    cursor.close()
    sys.exit() 

def menu_user_options(user_options):
    '''This function displays tasks menu. It asks the user to choose an action
    and runs until the accepted awnser is given. It returns
    user's choice of action '''
    choice = ''
    menu = '\nWhat would you like to do?:'
    for key in user_options:
        menu += f"\n{key}. {user_options[key]}"
    while choice not in user_options:
        print(menu) 
        choice = input("Enter your choice: ") 
        if choice in user_options:
            return choice
        else:
            print("\nInvalid choice. Please try again.")