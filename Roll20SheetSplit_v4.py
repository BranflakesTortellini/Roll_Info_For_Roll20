import csv
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import requests
import sys
sys.setrecursionlimit(2000)
import pandas as pd
import os
import re
import string


# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# specify the file name to import
raw_csv = "Rol20RollTotalsSplit.csv"

# check if the file exists in the working directory
if os.path.isfile(raw_csv):
    # if the file exists, import it using pd.read_csv
    df = pd.read_csv(raw_csv)
else:
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog window for selecting the CSV file
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

    # check if a file was selected and import it using pd.read_csv if so
    if file_path:
        df = pd.read_csv(file_path)
    else:
        # if no file was selected, exit the program
        sys.exit()




import re

def create_csv_files(df):
    # Create a list of unique rname values in the DataFrame
    rnames = df['rname'].unique().tolist()

    # Create a directory called "output_sorted_by_roll_name" in the current working directory if it does not exist
    if not os.path.exists("output_sorted_by_roll_name"):
        os.makedirs("output_sorted_by_roll_name")

    # Set the output directory as the current working directory
    os.chdir("output_sorted_by_roll_name")

    # Define the characters that are allowed in the save name
    allowed_chars = string.ascii_letters + string.digits + " _-"

    # Loop through the unique rname values and save each one as a separate CSV file in the output directory
    for rname in rnames:
        # replace all forward slashes (/) and hyphens (-) in rname with underscores (_)
        rname = rname.replace("/", "_")
        rname = rname.replace("-", "_")

        # Create a regular expression to match rows based on the rname
        rname_regex = re.escape(rname).replace("\-", "[_-]")

        # Create a simplified rname without any text inside parentheses or after '-save'
        simplified_rname = re.sub(r'\([^)]*\)|-?save.*', '', rname).strip()
        simplified_rname = re.sub('[^A-Za-z]+', '', simplified_rname)
        simplified_rname = ''.join(c for c in simplified_rname if c in allowed_chars)

        # Strip any special characters and integers from the rname
        stripped_rname = re.sub('[^A-Za-z]+', '', rname)
        stripped_rname = ''.join(c for c in stripped_rname if c in allowed_chars)

        # If the simplified rname is the same as the stripped rname, create only one csv file for that rname
        if simplified_rname == stripped_rname:
            rname_df = df[df["rname"].str.contains(rname_regex)]
            rname_df.to_csv(f"{stripped_rname}.csv", index=False)

        # Otherwise, create two csv files, one for the rname and another for the simplified rname
        else:
            rname_df = df[df["rname"].str.contains(rname_regex)]
            rname_df.to_csv(f"{stripped_rname}.csv", index=False)

            if simplified_rname:
                simplified_rname_df = df[df["rname"].str.contains(re.escape(simplified_rname))]
                simplified_rname_df.to_csv(f"{simplified_rname}_simplified.csv", index=False)

create_csv_files(df)





