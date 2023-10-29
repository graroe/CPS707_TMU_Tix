import os
import subprocess
import time
import pexpect
from pexpect import popen_spawn

#sets working directory
os.chdir("test/front_end_test/inputs")
#loop for each file in input directory.
for file_name in os.listdir():
    test_name = file_name.split('.')[0]
    print("running test " + test_name)
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
            prog.expect(expected[i], timeout = 5)
            o_file.write(prog.after.decode('utf-8') + "\n")
            i += 1
        


        