import os
from datetime import datetime
from event import event
#this can be removed if we just hand in back_end folder
os.chdir("back_end")

def handle_transaction(code, name, details):
    #create
    if (code == "03"):
        if name in master_dictionary:
            print("Constraint error: event named " + name +" already exists")
        else:
            master_dictionary[name] = event(date=details.date, avail_tickets=details.new_tickets)
    #delete
    elif (code == "05"):
        if not name in master_dictionary:
            print("Error: attempeted to delete event " + name +" that does not exist")
        else:
            master_dictionary.pop(name)
    #add/return
    elif (code == "02" or code == "04"):
        if not name in master_dictionary:
            print("Error: attempeted to increment tickets for event " + name +" that does not exist")
        else:
            new_total = master_dictionary[name].avail_tickets + details.new_tickets
            if new_total > 9999:
                print("Error: attempeted to increment tickets above maximum for event " + name)
            else:
                master_dictionary[name].avail_tickets = new_total
    #sell
    elif (code =="01"):
        if not name in master_dictionary:
            print("Error: attempeted to sell tickets for event " + name +" that does not exist")
        else:
            new_total = master_dictionary[name].avail_tickets - details.new_tickets
            if new_total < 0:
                print("Error: attempeted to sell more tickets than avialable for event " + name)
            else:
                master_dictionary[name].avail_tickets = new_total

def date_in_past(input):
    date = str(input)
    format = "%Y%m%d"
    date = datetime.strptime(date, format)
    current_datetime = datetime.today()
    if current_datetime > date:
        return True
    return False
    

#TODO: merge daily transaction files into merge file 
with open("master_events_file.txt") as mas_file:
    old_events = mas_file.readlines()
with open("merged_events_file.txt") as merg_file:
    new_events = merg_file.readlines()

#initialize master dictionary with old master events file
master_dictionary = {}
for event_line in old_events:
    fields = event_line.split()
    master_dictionary[fields[2]] = event(date=fields[0], avail_tickets=int(fields[1]))

#update master dictionary with entries from merged events file
for event_line in new_events:
    fields = event_line.split()
    code = fields[0]
    if code == "00":
        continue
    name = fields[1]
    details = event(date=fields[2], new_tickets=int(fields[3]))
    handle_transaction(code, name, details)

#remove all out-of-date events, write entries to output files
#TODO: sort master file by date
names = list(master_dictionary.keys())
with open("new_master_events_file.txt", 'w') as new_master_file:
    with open("current_events_file.txt", 'w') as current_file:
        for name in names:
            if date_in_past(master_dictionary[name].date):
                master_dictionary.pop(name)
            else:
                tix = str(master_dictionary[name].avail_tickets).zfill(4)
                name_spaced = name.ljust(15)
                new_master_file.write(" ".join([master_dictionary[name].date, tix, name_spaced])+ '\n')
                current_file.write(" ".join([name_spaced, tix]) + '\n')
        current_file.write("End             0000")

 


#temporary loop to check implementation
for entry in master_dictionary:
    event = master_dictionary[entry]
    print("name: " + entry + " date: " + event.date + " tickets: "+ str(event.avail_tickets))