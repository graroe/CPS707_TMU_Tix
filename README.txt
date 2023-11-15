Operational and test code are both designed to be run from the top level project directory (where this README file is located).
NOTE: Running any python files from a different working directory may cause errors.

For regular execution of Front End of TMU-tix, use this command: 'python3 ./front_end/front_end.py'
Terminal will prompt the user for input.

For the Front End testing suite use this command: 'python3 ./test/front_end_test/front_end_test_script.py'
may require installation of pexpect module, if not installed already ('pip install pexpect')
Terminal will output whether a test passed or failed. Detailed reports of failed tests can be found in the 'test_logs' directory.
Individual output files of the most recent test run can also be observed in the 'actual_outputs' directory.

For the Back End testing suite use this command: 'python3 ./test/back_end_test/back_end_test_script.py'
Terminal will output whether a test passed or failed. Failed cases will print the actual output and the expected output.