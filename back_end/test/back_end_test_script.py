#white box testing for back end system
import os

#ensure correct working directory
if os.getcwd()[-13:] == "back_end\\test":
    os.chdir("..")
elif not os.getcwd()[-8:] == "back_end":
    os.chdir("back_end")

print("Running basic block coverage test for sell transaction.")
print("Results:")
os.system("python3 test/sell_block_test.py")

print("Running decision coverage test for delete transaction.")
print("Results:")
os.system("python3 test/delete_decision_test.py")