import os
from datetime import datetime
import time
import pexpect
from pexpect import popen_spawn

time_now = datetime.now()
#creates new log file for whole test run
log_file_name = "test_run_" + time_now.strftime("%Y%m%d%H%M%S") +".txt"
log_file = open("test/front_end_test/test_logs/" + log_file_name, 'w')
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
    #stay in this dir to write actual outputs into
    os.chdir("../actual_outputs")
    with open(test_name +"_result.txt", 'w') as o_file:
        #spawn program, feed it inputs line by line, expects expected output lines, write resuts to file
        prog = pexpect.popen_spawn.PopenSpawn("python3 ../../../front_end/front_end.py" +
                                               " ../resources/current_events_example.txt" +" 20231020")
        i = 0
        prog.expect("Type 'login' to continue.")
        for input_line in inputs:
            prog.sendline(input_line)
            try:
                prog.expect(expected[i], timeout = 1)
            except pexpect.exceptions.TIMEOUT:
                #this occurs when expected does not match. Writes actual console output to file
                o_file.write(prog.before.decode('utf-8').replace("\r\n", "\n"))
                break
            o_file.write(prog.after.decode('utf-8') + "\n")
            i += 1  

    #compare actual written file to expected file and expected daily file (if applicable), ensure no diffs
    #failed test details written to log file
    with open(test_name +"_result.txt") as o_file:
        actual_output = o_file.read().rstrip('\n')
    os.chdir("../expected_outputs")
    with open(test_name + ".out") as e_file:
        expected_output = e_file.read().replace("\\n", "\n") #Comment out .replace... to see newline chars in expected
                                                                #note: may cause some tests to fail
    success = actual_output == expected_output
    daily_file_success = True
    actual_daily = "did not write"
    expected_daily = ""
    if os.path.exists(test_name + "_Daily.out"):
        with open(test_name + "_Daily.out") as e_daily_file:
            expected_daily = e_daily_file.read()
        if os.path.exists("../actual_outputs/daily_transaction.txt"):
            with open("../actual_outputs/daily_transaction.txt") as daily_file:
                actual_daily = daily_file.read()
        daily_file_success = expected_daily == actual_daily
    if success and daily_file_success:
        print("sucesss!\n")
        log_file.write(" test succeeded\n")  
    else:
        print("failed. check log file" + log_file.name + " for details\n")
        log_file.write(" test failed\n")
        if not success:
            log_file.write("console output did not match expected\n")
            comparison = "EXPECTED:\n" + expected_output + "\nACTUAL:\n" + actual_output +"\n******\n"
            log_file.write(comparison)
        if not daily_file_success:
            log_file.write("daily transaction file did not match expected\n")
            comparison = "EXPECTED:\n" + expected_daily + "\nACTUAL:\n" + actual_daily +"\n"
            log_file.write(comparison)
    
    #reset for beginning of loop
    if os.path.exists("../actual_outputs/daily_transaction.txt"):
        os.remove("../actual_outputs/daily_transaction.txt")
    log_file.write("\n")
    os.chdir("../inputs")
    
log_file.close()


