#This file is the out layer of the front end program. 
#front_end.py, state_manager.py, event.py, and current_events.txt
#should all be in the same directory.
#Then simply run front_end.py from the console to start the program.
#This module initializes a manager object and then controls the
#a loop to perform transactions.
import argparse
from state_manager import manager 

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("found", type=str, nargs='*')
args = arg_parser.parse_args()
found = args.found
s_manager = None
if len(found) > 0:
    if len(found)>1:
        pass
    s_manager = manager(current_events_filepath=found[0])
else:
    s_manager = manager()

print("Type 'login' to continue.")
while True:
    user_in = input()
    if user_in == "quit":
        break
    print(s_manager.perform_transaction(user_in))
exit