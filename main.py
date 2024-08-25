from authentication import authentication_menu, User
from tasks import tasks_menu

print("\nWelcome to 'On the Go To Do'!'")
# user = authentication_menu()
user = User(14,'John','Doe', 'johndoe')
tasks_menu(user)
