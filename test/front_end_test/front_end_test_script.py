import os
from datetime import datetime
import pexpect
from pexpect import popen_spawn

time_now = datetime.now()
#creates new log file for whole test run
log_file = open("test/front_end_test/test_logs/test_run_" + time_now.strftime("%Y%m%d%H%M%S") +".txt", 'w')
#sets working directory
os.chdir("test/front_end_test/inputs")
#loop for each file in input directory.
for file_name in os.listdir():
    test_name = file_name.split('.')[0]
    print("running test " + test_name)
    log_file.write(test_name+":")
    #split lines of test files, assign to lists
    with open(file_name) as file:
        inputs = file.read().splitlines()
    with open("../expected_outputs/" + test_name + ".out") as e_file:
        expected = e_file.read().splitlines()
    #make new file to store test result in 
    with open("../actual_outputs/" + test_name +"_result.txt", 'w') as o_file:
        os.chdir("../actual_outputs")  
        prog = pexpect.popen_spawn.PopenSpawn("python3 ../../../front_end/front_end.py")
        i = 0
        prog.expect("Type 'login' to continue.")
        for input_line in inputs:
            prog.sendline(input_line)
            try:
                prog.expect(expected[i], timeout = 2)
            except pexpect.exceptions.TIMEOUT:
                o_file.write("command on line " + str(i + 1) + " failed \n")
                break
            o_file.write(prog.after.decode('utf-8') + "\n")
            i += 1
            
    with open(test_name +"_result.txt") as o_file:
        actual_output = o_file.read()[:-1]
    os.chdir("../expected_outputs")
    with open(test_name + ".out") as e_file:
        expected_output = e_file.read()
    success = actual_output == expected_output
    if success:
        print("sucesss!")
        log_file.write(" test succeeded\n")  
    else:
        print("fail")
        log_file.write(" test failed\n")
        comparison = "expected:\n" + expected_output + "\n******\n" + "actual:\n" + actual_output +"\n\n"
        print(comparison)
        log_file.write(comparison)
    os.chdir("../inputs")
    
log_file.close()


