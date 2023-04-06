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

def split_dataframe_by_dietype(df):
    # Create character_output folder if it does not exist
    output_folder = 'DieType_output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Create a dictionary to hold the split dataframes
    split_dfs = {}

    # Loop over the unique DieType values in the dataframe
    for DieType in df['DieType'].unique():
        # Get all the rows with the current DieType value
        temp_df = df[df['DieType'] == DieType]

        # If there is more than one row with this DieType value, split the data
        if len(temp_df) > 1:
            # Remove any special characters from the DieType value to create a filename
            filename = "".join(x for x in DieType if x.isalnum()) + ".csv"

            # Add the current DieType value to the dictionary of split dataframes
            split_dfs[DieType] = temp_df

            # If the current DieType value has any similar values, add them to the same split dataframe
            for similar_DieType in df[df['DieType'].str.contains(DieType, regex=False) & (df['DieType'] != DieType)]['DieType'].unique():
                if any([similar_DieType[i:i+4] in DieType for i in range(len(similar_DieType)-3)]):
                    split_dfs[DieType] = pd.concat([split_dfs[DieType], df[df['DieType'] == similar_DieType]])

            # Save the split dataframe to a CSV file
            split_dfs[DieType].to_csv(os.path.join(output_folder, filename), index=False)

        # If there is only one row with this DieType value, do not split the data and skip to the next DieType value
        else:
            continue

    # If there are no rows with the same DieType value, save the entire dataframe to a CSV file
    if len(split_dfs) == 0:
        df.to_csv(os.path.join(output_folder, "all_data.csv"), index=False)

    # Otherwise, save a combined CSV file for each group of split dataframes
    else:
        for DieType, split_df in split_dfs.items():
            # Get all similar DieType values
            similar_DieTypes = []
           #for other_DieType in df['DieType'].unique():
           #     if DieType != other_DieType and len(set(DieType.split()) & set(other_DieType.split())) > 0:
           #         similar_DieTypes.append(other_DieType)
                        
            # Combine dataframes with similar DieYtypes
            if len(similar_DieTypes) > 0:
                similar_DieTypes.append(DieType)
                combined_df = df[df['DieType'].isin(similar_DieTypes)]
                common_term = ' '.join(set(DieType.split()).intersection(*[set(name.split()) for name in similar_DieTypes]))
                common_suffix = "-".join([suffix for suffix in ["OneHanded", "TwoHanded", "save"] if DieType.endswith(suffix)])
                combined_filename = "".join(x for x in common_term if x.isalnum()) + common_suffix + "_combined.csv"
                combined_df.to_csv(os.path.join("DieType_output", combined_filename), index=False)



split_dataframe_by_dietype(df)