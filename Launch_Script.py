import os
import subprocess

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# specify the relative path to the script
script1_path = "Roll20ChatJsonToDF_v3.py"
script2_path = "Roll20DataOrganization_v1.py" 
script3_path = "Roll20AddStatAve_v3.py"
script4_path = "Roll20SheetSplit_rname_v7.py"
script5_path = "Roll20SheetSplit_Charname_v2.py"
script6_path = "Roll20SheetSplit_DieType_v1.py"
script7_path = "Roll20Add_Row_Numbers_v2.py"


# Pulls character and roll data from Roll20JsonFile - use "chatarchive"
subprocess.run(["python", script1_path])

#clean csv data to make numbers easier to work with
subprocess.run(["python", script2_path])

#adds statistical average based for first roll pair of a given action
subprocess.run(["python", script3_path])

#Split data into differnt sheets based on roll name
subprocess.run(["python", script4_path])

#Split data into differnt sheets based on character name
subprocess.run(["python", script5_path])

#Split data into differnt sheets based on DieType - non exhaustive, looks at first roll of action
subprocess.run(["python", script6_path])

#adds roll counts both for action type and number of times player has rolled that action
subprocess.run(["python", script7_path])


