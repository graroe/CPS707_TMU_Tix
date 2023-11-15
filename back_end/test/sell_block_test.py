import os
import subprocess

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
bytes = subprocess.check_output("python3 back_end.py")
console_lines = bytes.decode().splitlines()
with open("test/expected_outputs/sell_block_test.out") as e_file:
    expecteds = e_file.readlines()

for i in range(len(expecteds)):
    if expecteds[i].strip() == console_lines[i]:
        print("test case " + str(i + 1) + " passed")
    else:
        print("test case " + str(i + 1) + " failed.\nExpected: " + expecteds[i] + "\nActual: " + console_lines[i])

with open("master_events_file.txt") as master_file:
    master_contents = master_file.read()
with open("to_front_end/current_events_file.txt") as c_file:
    current_contents = c_file.read()
with open("test/expected_outputs/sell_master_event.out") as e_m_file:
    expected_master_file = e_m_file.read()
with open("test/expected_outputs/sell_current_event.out") as e_c_file:
    expected_current_contents = e_c_file.read()

if master_contents == expected_master_file and current_contents == expected_current_contents:
    print("test case " + str(i + 2) + " passed")
else:
    print("test case " + str(i + 1) + " failed.\nExpected master file: " + expected_master_file + "\nActual: " + master_contents)
    print("Expected current file: " + expected_current_contents + "\nActual: " + current_contents)

#cleanup
for file_name in os.listdir("from_front_end"):
    os.remove("from_front_end/" + file_name)