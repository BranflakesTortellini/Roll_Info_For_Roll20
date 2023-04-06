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

def split_dataframe_by_charname(df):
    # Create character_output folder if it does not exist
    output_folder = 'character_output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Create a dictionary to hold the split dataframes
    split_dfs = {}

    # Loop over the unique charname values in the dataframe
    for charname in df['charname'].unique():
        # Get all the rows with the current charname value
        temp_df = df[df['charname'] == charname]

        # If there is more than one row with this charname value, split the data
        if len(temp_df) > 1:
            # Remove any special characters from the charname value to create a filename
            filename = "".join(x for x in charname if x.isalnum()) + ".csv"

            # Add the current charname value to the dictionary of split dataframes
            split_dfs[charname] = temp_df

            # If the current charname value has any similar values, add them to the same split dataframe
            for similar_charname in df[df['charname'].str.contains(charname, regex=False) & (df['charname'] != charname)]['charname'].unique():
                if any([similar_charname[i:i+4] in charname for i in range(len(similar_charname)-3)]):
                    split_dfs[charname] = pd.concat([split_dfs[charname], df[df['charname'] == similar_charname]])

            # Save the split dataframe to a CSV file
            split_dfs[charname].to_csv(os.path.join(output_folder, filename), index=False)

        # If there is only one row with this charname value, do not split the data and skip to the next charname value
        else:
            continue

    # If there are no rows with the same charname value, save the entire dataframe to a CSV file
    if len(split_dfs) == 0:
        df.to_csv(os.path.join(output_folder, "all_data.csv"), index=False)

    # Otherwise, save a combined CSV file for each group of split dataframes
    else:
        for charname, split_df in split_dfs.items():
            # Get all similar charname values
            similar_charnames = []
            for other_charname in df['charname'].unique():
                if charname != other_charname and len(set(charname.split()) & set(other_charname.split())) > 0:
                    similar_charnames.append(other_charname)
                        
            # Combine dataframes with similar rnames
            if len(similar_charnames) > 0:
                similar_charnames.append(charname)
                combined_df = df[df['charname'].isin(similar_charnames)]
                common_term = ' '.join(set(charname.split()).intersection(*[set(name.split()) for name in similar_charnames]))
                common_suffix = "-".join([suffix for suffix in ["OneHanded", "TwoHanded", "save"] if charname.endswith(suffix)])
                combined_filename = "".join(x for x in common_term if x.isalnum()) + common_suffix + "_combined.csv"
                combined_df.to_csv(os.path.join("character_output", combined_filename), index=False)






split_dataframe_by_charname(df)