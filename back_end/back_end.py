import os
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

#TODO: merge daily transaction files into merge file 
with open("master_events_file.txt") as mas_file:
    old_events = mas_file.readlines()
with open("merged_events_file.txt") as merg_file:
    new_events = merg_file.readlines()

master_dictionary = {}
for event_line in old_events:
    fields = event_line.split()
    master_dictionary[fields[2]] = event(date=fields[0], avail_tickets=int(fields[1]))

for event_line in new_events:
    fields = event_line.split()
    code = fields[0]
    if code == "00":
        continue
    name = fields[1]
    details = event(date=fields[2], new_tickets=int(fields[3]))
    handle_transaction(code, name, details)

#
for entry in master_dictionary:
    event = master_dictionary[entry]
    print("name: " + entry + " date: " + event.date + " tickets: "+ str(event.avail_tickets))
      

