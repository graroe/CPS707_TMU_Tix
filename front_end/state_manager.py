from datetime import datetime

session_types = ["sales","admin"]
session_full_name = {"sales":"Sales agent", "admin":"Admin"}

class manager():
    def __init__(self):
        self.login_state = False
    
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
            while event_name == "" or len(event_name) > 15:
                event_name = input("Enter new event name (max 15 chars): ")
            
            event_date = ""
            while not self.valid_date(event_date): 
                event_date = input("Enter date of event (format YYYYMMDD): ")
            
            ticket_amount = -1
            while ticket_amount < 0 or ticket_amount > 9999:
                ticket_amount = int(input("Enter number of available tickets (max 9999): "))
            
            ### TODO: write event_name, event_date, ticket_amount values into memory

            return "Event " + event_name + " created."
        else:
            return "Access denied. Must be in admin mode."
    

    def handle_add(self):
        pass

    def handle_delete(self):
        pass

    def handle_sell(self):
        pass

    def handle_return(self):
        pass
    
    ### HELPER FUNCTIONS ###

    def load_current_events(self):
        pass

    def write_current_events(self):
        pass

    def valid_date(self, input):
        date = str(input)
        format = "%Y%m%d"
        
        result = True

        try:
            result = bool(datetime.strptime(date, format))
        except ValueError:
            result = False
        
        return result

    
    