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

    def handle_transaction(self, raw_str):
        if raw_str == "login":
            return self.handle_login()
        elif raw_str == "logout":
            return self.handle_logout()
        elif raw_str == "create" and self.login_state != False:
            return self.handle_create()
        else:
            return False
        
    def handle_login(self):
        if self.login_state != False:
            return "Already logged in."
        new_session = ""
        while not new_session in session_types:
            new_session = input("Enter session type (sales or admin):")
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
            return "HELLO"
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
    
    def load_current_events(self):
        pass

    def write_current_events(self):
        pass

    
    