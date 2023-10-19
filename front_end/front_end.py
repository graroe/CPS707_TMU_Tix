
from state_manager import manager 

manager = manager()
print("Log in to continue")
while True:
    user_in = input()
    if user_in == "quit":
        break
    print(manager.perform_transaction(user_in))

print("Session terminated.")
exit
    