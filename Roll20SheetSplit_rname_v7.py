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


import os
import pandas as pd

def split_dataframe_by_rname(df):
    # Create roll_output folder if it does not exist
    output_folder = 'roll_output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Create a dictionary to hold the split dataframes
    split_dfs = {}

    # Loop over the unique rname values in the dataframe
    for rname in df['rname'].unique():
        # Get all the rows with the current rname value
        temp_df = df[df['rname'] == rname]

        # If there is more than one row with this rname value, split the data
        if len(temp_df) > 1:
            # Remove any special characters from the rname value to create a filename
            filename = "".join(x for x in rname if x.isalnum()) + ".csv"

            # Add the current rname value to the dictionary of split dataframes
            split_dfs[rname] = temp_df

            # If the current rname value has any similar values, add them to the same split dataframe
            for similar_rname in df[df['rname'].str.contains(rname, regex=False) & (df['rname'] != rname)]['rname'].unique():
                if any([similar_rname[i:i+4] in rname for i in range(len(similar_rname)-3)]):
                    split_dfs[rname] = pd.concat([split_dfs[rname], df[df['rname'] == similar_rname]])

            # Save the split dataframe to a CSV file
            split_dfs[rname].to_csv(os.path.join(output_folder, filename), index=False)

        # If there is only one row with this rname value, do not split the data and skip to the next rname value
        else:
            continue

    # If there are no rows with the same rname value, save the entire dataframe to a CSV file
    if len(split_dfs) == 0:
        df.to_csv(os.path.join(output_folder, "all_data.csv"), index=False)

    # Otherwise, save a combined CSV file for each group of split dataframes
    else:
        for rname, split_df in split_dfs.items():
            # Get all similar rname values
            similar_rnames = []
            for other_rname in df['rname'].unique():
                if rname != other_rname and len(set(rname.split()) & set(other_rname.split())) > 0:
                    similar_rnames.append(other_rname)
                        
            # Combine dataframes with similar rnames
            if len(similar_rnames) > 0:
                similar_rnames.append(rname)
                combined_df = df[df['rname'].isin(similar_rnames)]
                common_term = ' '.join(set(rname.split()).intersection(*[set(name.split()) for name in similar_rnames]))
                common_suffix = "-".join([suffix for suffix in ["OneHanded", "TwoHanded", "save"] if rname.endswith(suffix)])
                combined_filename = "".join(x for x in common_term if x.isalnum()) + common_suffix + "_combined.csv"
                combined_df.to_csv(os.path.join("roll_output", combined_filename), index=False)






split_dataframe_by_rname(df)