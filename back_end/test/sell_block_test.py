import os

#ensure correct current working directory
if os.getcwd()[-13:] == "back_end\\test":
    os.chdir("..")
elif not os.getcwd()[-8:] == "back_end":
    os.chdir("back_end")

#write input file copies to directories retrievable by back_end.py
for file_name in os.listdir("test/sell_block_test_files/"):
    with open("test/sell_block_test_files/" + file_name) as in_file:
        contents = in_file.read()
    if file_name.startswith("daily_transaction_file"):
        with open("from_front_end/" + file_name, 'w') as new_file:
            new_file.write(contents)
    elif file_name.startswith("master_events_file"):
        with open(file_name, 'w') as new_file:
            new_file.write(contents)

#run program
os.system("python3 back_end.py")

#cleanup
for file_name in os.listdir("from_front_end"):
    os.remove("from_front_end/" + file_name)