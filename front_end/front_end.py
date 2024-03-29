#This file is the out layer of the front end program. 
#front_end.py, state_manager.py, event.py, and current_events.txt
#should all be in the same directory.
#Then simply run front_end.py from the console to start the program.
#This module initializes a manager object and then controls the
#a loop to perform transactions.
import argparse
import time
from state_manager import manager 

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("found", type=str, nargs='*')
args = arg_parser.parse_args()
found = args.found
s_manager = None
#Check command line arguments optional and/or test properties
#argument 1: sets filepath for reading current events file (useful for testing)
if len(found) == 1:
    s_manager = manager(current_events_filepath=found[0])
#argument 2: sets a fake date time. ONLY useful for testing (so test files need not be updated constantly to "valid" dates)
elif len(found) > 1 :
    s_manager = manager(current_events_filepath=found[0], test_date_time=found[1])
#no arguments: default settings
else:
    s_manager = manager()

print("Type 'login' to continue.")
while True:
    user_in = input()
    if user_in == "quit":
        break
    print(s_manager.perform_transaction(user_in))
exit(0)