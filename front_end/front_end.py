#This file is the out layer of the front end program. 
#front_end.py, state_manager.py, event.py, and current_events.txt
#should all be in the same directory.
#Then simply run front_end.py from the console to start the program.
#This module initializes a manager object and then controls the
#a loop to perform transactions.
from state_manager import manager 

manager = manager()
print("Type 'login' to continue.")
while True:
    user_in = input()
    if user_in == "quit":
        break
    print(manager.perform_transaction(user_in))
exit