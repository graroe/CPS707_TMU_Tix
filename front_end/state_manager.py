from datetime import datetime
from event import event
import re

session_types = ["sales","admin"]
session_full_name = {"sales":"Sales agent", "admin":"Admin"}
daily_transaction_filepath = "daily_transaction.txt"
current_events_filepath = "front_end/current_events.txt"
current_events_endline = "End             0000"

class manager():
    ### initializes a session
    def __init__(self):
        self.login_state = False
        self.escape_text = "Transaction canceled"
        self.events = {}
        self.transaction_records = []
    
    ### throws errors for invalid commands or if the user is not logged in.
    def perform_transaction(self, raw_str):
        result = self.handle_transaction(raw_str)
        if result == False:
            if self.login_state == False: 
                        return "Invalid command. Log in to continue."
            else:
                return "Unrecognized command."
        return result

    ### calls transaction handlers based on raw_str
    def handle_transaction(self, raw_str):
        if raw_str == "login":
            return self.handle_login()
        elif raw_str == "logout":
            return self.handle_logout()
        elif raw_str == "create" and self.login_state != False:
            return self.handle_create()
        elif raw_str == "add" and self.login_state != False:
            return self.handle_add()
        elif raw_str == "delete" and self.login_state != False:
            return self.handle_delete()
        elif raw_str == "sell" and self.login_state != False:
            return self.handle_sell()
        elif raw_str == "return" and self.login_state != False:
            return self.handle_return()
        else:
            return False

    ### TRANSACTION HANDLERS ###   

    # user will select either sales or admin permissions
    # error message returned if already logged in.
    def handle_login(self):
        if self.login_state != False:
            return "Already logged in."
        new_session = ""
        while not new_session in session_types:
            new_session = input("Enter session type (sales or admin): ")
        self.login_state = new_session
        self.load_current_events()
        return session_full_name[new_session] + " login successful"
    
    # session transactions are written to the Event Transaction File
    # error message returned if not logged in.
    def handle_logout(self):
        if self.login_state == False:
            return "Not currently logged in."
        self.login_state = False
        self.write_transaction_file()
        return "Session terminated.\nType 'login' to continue."
    
    # user must be in admin mode to perform this transaction
    # user prompted for a new unique name, a valid date and a number of tickets not exceeding 9999 tickets.
    def handle_create(self):
        if self.login_state == "admin":            
            event_name = ""
            while event_name == "":
                event_name = input("Enter new event name (max 15 chars): ")
                if self.escape_character(event_name):
                    return self.escape_text
                if len(event_name) > 15:
                    event_name = ""
                    print("Character limit exceeded")
                if event_name in self.events.keys():
                    event_name = ""
                    print("Event name already exists")
            
            event_date = ""
            while not self.valid_date(event_date): 
                event_date = input("Enter date of event (format YYYYMMDD): ")
                if self.escape_character(event_date):
                    return self.escape_text
            
            ticket_amount = -1
            while ticket_amount < 0 or ticket_amount > 9999:
                user_input = input("Enter number of available tickets (max 9999): ")
                if self.escape_character(user_input):
                    return self.escape_text

                if not user_input.isnumeric():
                    ticket_amount = -1
                else:
                    ticket_amount = int(user_input)
            
            self.events[event_name] = event(date=event_date, new_tickets=ticket_amount)
            self.transaction_records.append(self.construct_record("03", event_name, ticket_amount, date = event_date))
            return "Event " + str(event_name) + " created."
        else:
            return "Access denied. Must be in admin mode."
    
    # user must be in admin mode to perform this transaction
    # user prompted for an existing event name, and a number of tickets to add such that the total number does not exceed 9999 tickets.
    def handle_add(self):
        if self.login_state == "admin":
            event_name = ""
            while event_name == "":
                event_name = input("Enter event name: ")
                if self.escape_character(event_name):
                    return self.escape_text
                if not event_name in self.events.keys():
                    event_name = ""
                    print("Event not found.")
            
            event = self.events[event_name]
            event_date = event.date   
            current_amount = event.avail_tickets + event.new_tickets
            new_amount = -1

            print("Event Date: " + str(event_date))
            print("Current number of tickets: " + str(current_amount))
            while new_amount < 0 or new_amount + current_amount >= 9999:
                user_input = input("Enter number of tickets to add: ")
                if self.escape_character(user_input):
                    return self.escape_text

                if not user_input.isnumeric():
                    new_amount = -1
                elif int(user_input) + current_amount > 9999:
                    new_amount = -1
                    print("Cannot exceed 9999 tickets.")
                else:
                    new_amount = int(user_input)
            
            new_total = new_amount + current_amount
            event.new_tickets = new_total
            self.transaction_records.append(self.construct_record("04", event_name, new_amount, date = event_date))
            return str(new_amount) + " tickets added. New total: " + str(new_total)
        else:
            return "Access denied. Must be in admin mode."
            
    # user must be in admin mode to perform this transaction
    # user prompted for an existing event name, and then to type 'delete' to confirm the transaction.
    def handle_delete(self):
        if self.login_state == "admin":            
            event_name = ""
            while event_name == "":
                event_name = input("Enter event name: ")
                if self.escape_character(event_name):
                    return self.escape_text
                if not event_name in self.events.keys():
                    event_name = ""
                    print("Event not found.")
            
            while True:
                user_input = input("Enter the word 'delete' to confirm: ")
                if self.escape_character(user_input):
                    return self.escape_text
                if user_input == "delete":
                    break
                user_input = ""

            self.transaction_records.append(self.construct_record("05", event_name, 0))
            self.events.pop(event_name)           

            return "Event " + str(event_name) + " deleted."
        else:
            return "Access denied. Must be in admin mode."

    # user prompted for an existing event name and number of tickets to be sold.
    # restricted to 8 tickets per transaction in sale agent mode.
    def handle_sell(self):
        event_name = ""
        while event_name == "":
            event_name = input("Enter event name: ")
            if self.escape_character(event_name):
                return self.escape_text
            if not event_name in self.events.keys():
                event_name = ""
                print("Event not found.")
        
        event = self.events[event_name]
        current_amount = event.avail_tickets
        new_amount = -1

        print("Current number of tickets: " + str(current_amount))
        while new_amount < 0:
            user_input = input("Enter number of tickets to sell: ")
            if self.escape_character(user_input):
                return self.escape_text

            if not user_input.isnumeric():
                new_amount = -1
            elif int(user_input) > current_amount:
                new_amount = -1
                print("Not enough tickets.")
            else:
                if self.login_state == "admin" or (self.login_state == "sales" and int(user_input) <= 8):
                    new_amount = int(user_input)
                else:
                    new_amount = -1
                    print("Maximum of 8 Tickets can be sold per transaction")

        new_total = current_amount - new_amount
        event.avail_tickets = new_total
        self.transaction_records.append(self.construct_record("01", event_name, new_amount))
        return str(new_amount) + " tickets sold. New total: " + str(new_total)

    # user prompted for an existing event name and number of tickets to be returned.
    # restricted to 8 tickets per transaction in sale agent mode.
    def handle_return(self):
        event_name = ""
        while event_name == "":
            event_name = input("Enter event name: ")
            if self.escape_character(event_name):
                return self.escape_text
            if not event_name in self.events.keys():
                event_name = ""
                print("Event not found.")
        
        event = self.events[event_name]
        current_amount = event.avail_tickets
        new_amount = -1

        print("Current number of tickets: " + str(current_amount))
        while new_amount < 0:
            user_input = input("Enter number of tickets to return: ")
            if self.escape_character(user_input):
                return self.escape_text

            if not user_input.isnumeric():
                new_amount = -1
            elif int(user_input) + current_amount > 9999:
                new_amount = -1
                print("Total tickets cannot exceed 9999.")
            else:
                if self.login_state == "admin" or (self.login_state == "sales" and int(user_input) <= 8):
                    new_amount = int(user_input)
                else:
                    new_amount = -1
                    print("Maximum of 8 Tickets can be returned per transaction")
        
        new_total = current_amount + new_amount
        event.avail_tickets = new_total
        self.transaction_records.append(self.construct_record("02", event_name, new_amount))
        return str(new_amount) + " tickets returned. New total: " + str(new_total)
    
    ###                  ###
    ### HELPER FUNCTIONS ###
    ###                  ###
    
    # checks if the given input is the escape character
    def escape_character(self, input):
        if input == "!q" or input == "!Q":
            return True
        return False

    # checks if the given input is a valid date, and is after today and no more than two years from today
    def valid_date(self, input):

        date = str(input)
        format = "%Y%m%d"
        result = True

        try:
            date = datetime.strptime(date, format)
            result = bool(date)
        except ValueError:
            result = False
        
        upper_limit = datetime(datetime.today().year + 2, datetime.today().month, datetime.today().day)
        if result == True and (datetime.today() > date or date > upper_limit):
            print("Date must be between tomorrow and 2 years in the future.")
            result = False

        return result

    # contructs transaction record string
    def construct_record(self, code, name, tickets, date="00000000"):
        return " ".join([code, name.ljust(15), date, str(tickets).zfill(4)])

    # loads data from event transaction file and populates a dictionary of Events objects
    def load_current_events(self):
        with open(current_events_filepath) as file:
            loaded = file.read().splitlines()
        for line in loaded:
            if line == current_events_endline:
                break
            words = re.split(' +', line)
            self.events[words[0]] = event(avail_tickets=int(words[1]))
    
    # writes list of transaction records to file
    def write_transaction_file(self):
        with open(daily_transaction_filepath, 'w') as file:
            for record in self.transaction_records:
                file.write(record + '\n')
            file.write(self.construct_record("00", "", 0))
                                             

    