import os
import subprocess

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# specify the relative path to the script
script1_path = "Roll20ChatJsonToDF_v2.py"
script2_path = "Roll20DataOrganization_v1.py"
script3_path = "Roll20SheetSplit.py"
script3_path = "Roll20StatCalc.py"

# run the script as a subprocess
subprocess.run(["python", script1_path])

#clean csv data to make numbers easier to work with
subprocess.run(["python", script2_path])

#Split data into differnt sheets based on roll name
#subprocess.run(["python", script3_path])

#calculate various stats from split dataset
#subprocess.run(["python", script4_path])