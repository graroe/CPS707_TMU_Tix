import os
import subprocess
import time
import pexpect
from pexpect import popen_spawn

#FYI added command line arg paring to front_end to specify a test current_events file
    #I tried it and it works, but for simplicity right now i'm not using it yet

#sets working directory
os.chdir("test/front_end_test/inputs")
#loop for each file in input directory. currently there is only 1
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
        
        #TODO: HERE IS WHERE THE TROUBLE BEGINS
        #The idea is to start the front end program, 
        #feed it an input line, capture its response (can write to result file but haven't got there yet), 
        #and repeat

        #ATTEMPT 1: subprocess.Popen
        #successfully starts subprocesses, can read and write to some degree
        #Issues: cannot seem to interleave stdin and stdout methods
        #   appaently they can get deadlocked
        #   something about stdout buffer fro subprocesses being a certain size?
        #       tried messing with bufsize parameter and flush commands below, didn't help
        #tried with all writes first, then reads after
        #   kinda works, but somehow subprocess continuosly receiving EOF chars, messing up output
        #       added a catch block to front_end.py for now to print a message instead of crashing
        #       may be result of input stream closing? but seems to happen even between stdin calls
        #   This is still the closest I've gotten I think.
        #Notes:
        #   test_run.poll() will return None if subprocess still running
        #   Google will tell you to use subprocess.communicate() instead of stdin/stdout
        #       But this does not work for our purposes as it just inputs 1 command, then closes stream
        #           same with subprocess.run() in place of subprocess.Popen
        '''
        with subprocess.Popen(['python', "../../../front_end/front_end.py"], stderr=subprocess.PIPE, #bufsize=0, cwd=".",
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, text=True) as test_run:
            #not sure if using flush properly? dosnt change much.
            #added sleeps to ensure program's prompt appears before input
            #tried using hard coded strings for now just to get it working
            #test_run.stdout.flush()
            time.sleep(0.3)
            test_run.stdin.write("login")
            time.sleep(0.3)
            #test_run.stdin.flush()
            test_run.stdin.write("sales")
            time.sleep(0.3)
            test_run.stdin.write("logout")
            time.sleep(0.3)
            test_run.stdin.write("quit")
            test_run.stdin.close()
            print(test_run.poll())
            while True:
                print(test_run.stdout.readline())
                time.sleep(1)
           
            #Attempt 1.1: similar to above but input is in a loop
            #and inputs are from the list contructed from input file 
        '''
        '''
            for input in inputs:
                #print("loop begin:")
                print(test_run.stdout.readline())
                #test_run.stdout.flush()
                time.sleep(0.2)
                print(input)
                print(test_run.stdin.write(input))
                #print(test_run.stdin.flush())
            print(test_run.stdin.write("quit"))
            #test_run.stdin.close()
            
            #print(test_run.stdout.readline())
            #print(test_run.poll())
            #test_run.stdin.write("quit")
            #test_run.stdin.flush()
        '''

    #ATTEMPT 2: pexpect
    #you might have more luck with this one because part of the problem might be Windows compatibility?
    #usual way to use this library is pexpect.spawn instead of pexpect.popen_spawn.PopenSpawn
        #but apparently pexpect.spawn is not compatible with Windows os
    #docs: https://pexpect.readthedocs.io/en/stable/overview.html
    #looks like it should be easy, but was not working for me
    #prog.sendline() sends input (prog being my variable name. I dunno why I changed it each time)
    #prog.expect(x) -> x matches paramater to console response, I think
            #not sure what's supposed to happen if they don;t, but for me i think it kinda stopped.
        #may need to append newlines on sendline and/or expect, not sure, not sure
        #seems like expect() as accepts regex input, but don't just use .* because that'll match ""
            #maybe .*/n would work 
    #there is also a prog.readlines() function to atually read console output
        #but should be same as what we're putting in to expect() function paramet
        #maybe that's what we call when expect() fails?
    
    #Before we get to my version, here's a quick one I whipped up that
    #uses the version windows hates
    # I really thought it would be this simple.
    #try uncommenting and running, maybe it'll work!
    '''
    prog=pexpect.spawn("python ../../../front_end/front_end.py")
    i = 0
    prog.expect("Type 'login' to continue.\n")
    for input_line in inputs:
        prog.sendline(input_line)
        sleep()
        prog.expect(expected[i])
        i += 1
    '''

    #ok, and now the windows-compatible version... 
    #which seems to send lines but not really receive the reponses
    '''
    #prog = pexpect.popen_spawn.PopenSpawn("python ../../../front_end/front_end.py /test/front_end_test/resources/test/current_events_example.txt")
    print(prog.expect("Type 'login' to continue.\n"))
    for input_line in inputs:
        #print(prog.before)
        #print(prog.after)
        prog.sendline(input_line)
        print("fffff")
        #print(prog.readline())
        print(prog.expect(".*\n"))
    #print(prog.before)
    #print(prog.after)
    #print(prog.read())
    '''

    #attempt 2.2
    #since i wasn't getting the console output properly, tried 
    #this again but instead of spawning the python program istaelf
    #spawned a command line instance and used it to call python program
    #this did not work either
    '''
    child = pexpect.popen_spawn.PopenSpawn('cmd', timeout=1)
    child.expect("Microsoft Windows [Version 10.0.22621.2428]\r\n")
    child.send("python ../../../front_end/front_end.py")
    child.expect("Type 'login' to continue.")
    
    print(child.readline())
    print(child.readlines())
    '''
    

    #ATTEMPT 3: os.popen 
    #This just does not work because it can only be readable or writable, not both at the same time.
    '''
    pipe = os.popen('python ../../../front_end/front_end.py', 'w')
    a = pipe.readline()
    print(a)
    print(pipe.writable())
    os.system("echo login")
    a = pipe.readline()
    
    print(a)
    os.system("echo sales")
    a = pipe.readline()
    print(a)
    a = pipe.readline()
    print(a)
    
    pipe.close()
    '''
        
    