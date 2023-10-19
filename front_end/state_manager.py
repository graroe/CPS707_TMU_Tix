from datetime import datetime

session_types = ["sales","admin"]
session_full_name = {"sales":"Sales agent", "admin":"Admin"}

class manager():
    def __init__(self):
        self.login_state = False
        self.escape_text = "Transaction canceled"
    
    def perform_transaction(self, raw_str):
        result = self.handle_transaction(raw_str)
        if result == False:
            if self.login_state == False: 
                        return "Invalid command. Log in to continue."
            else:
                return "Unrecognized command."
        return result


    ### COMMAND HANDLER ###

    def handle_transaction(self, raw_str):
        if raw_str == "login":
            return self.handle_login()
        elif raw_str == "logout":
            return self.handle_logout()
        elif raw_str == "create" and self.login_state != False:
            return self.handle_create()
        elif raw_str == "add" and self.login_state != False:
            return self.handle_add()
        else:
            return False

    ### TRANSACTION HANDLERS ###   

    def handle_login(self):
        if self.login_state != False:
            return "Already logged in."
        new_session = ""
        while not new_session in session_types:
            new_session = input("Enter session type (sales or admin): ")
        self.login_state = new_session
        self.load_current_events()
        return session_full_name[new_session] + " login successful"
    
    def handle_logout(self):
        if self.login_state == False:
            return "Not currently logged in."
        self.login_state = False
        self.write_current_events()
        return "Session terminated.\nType 'login' to continue."
    
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

            ### TODO: Ensure event_name is unique compared to existing events
            ### if event_name == event[i]:
            ###     event_name = ""
            ###     print("Event name already exists")
            
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
            
            ### TODO: write values into Event object

            return "Event " + event_name + " created."
        else:
            return "Access denied. Must be in admin mode."
    
    def handle_add(self):
        if self.login_state == "admin":
            event_name = ""

            while event_name == "":
                event_name = input("Enter event name: ")
                if self.escape_character(event_name):
                    return self.escape_text
            ### TODO: ensure event_name exists in memory
            ### if event_name is not in event_list:
            ###     event_name = ""
            ###     print("Event not found.")
            
            event_date = 20231031   ### TODO: change to read from memory for specific event
            current_amount = 10     ### TODO: change to read from memory for specific event
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
            
            ### TODO: write values into Event object and buffer
            ###       ensure that new_amount is added to a separate buffer so it can't be sold in the same session
            new_total = new_amount + current_amount
            return str(new_amount) + " tickets added. New total: " + str(new_total)
        else:
            return "Access denied. Must be in admin mode."

    def handle_delete(self):
        pass

    def handle_sell(self):
        pass

    def handle_return(self):
        pass
    
    ###                  ###
    ### HELPER FUNCTIONS ###
    ###                  ###
    
    def escape_character(self, input):
        if input == "!q" or input == "!Q":
            return True
        return False

    def valid_date(self, input):
        ### TODO: Implement that dates must be in the future and within two years from today

        date = str(input)
        format = "%Y%m%d"
        result = True

        try:
            result = bool(datetime.strptime(date, format))
        except ValueError:
            result = False
        
        return result

    def load_current_events(self):
        pass

    def write_current_events(self):
        pass
    