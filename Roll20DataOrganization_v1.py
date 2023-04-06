import csv
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import requests
import sys
sys.setrecursionlimit(2000)
import pandas as pd
import os

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# specify the file name to import
raw_csv = "Roll20InitialJsonToDF.csv"

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




#Split roll data into multiple colums:


def split_roll_data(df):
    # split the result column into separate columns
    df_natrolls = df['result'].str.split(',', expand=True)
    df_natrolls.columns = [f'natroll_{i+1}' for i in range(df_natrolls.shape[1])]

    # remove special characters from the new columns
    df_natrolls = df_natrolls.apply(lambda x: x.str.replace(r'[,"\[\]\(\)\'"]', '', regex=True))

    # strip whitespace from the new columns
    df_natrolls = df_natrolls.apply(lambda x: x.str.replace('\s+', '', regex=True))

    # concatenate the new columns with the original dataframe
    df2 = pd.concat([df, df_natrolls], axis=1)

    # split the total column into separate columns
    df_totals = df['total'].str.split(',', expand=True)
    df_totals.columns = [f'totalroll_{i+1}' for i in range(df_totals.shape[1])]

    # remove special characters from the new columns
    df_totals = df_totals.apply(lambda x: x.str.replace(r'[,"\[\]\(\)\'"]', '', regex=True))

    # strip whitespace from the new columns
    df_totals = df_totals.apply(lambda x: x.str.replace('\s+', '', regex=True))

    # concatenate the new columns with the original dataframe
    df3 = pd.concat([df2, df_totals], axis=1)

    # calculate the modtotal columns
    for i in range(1, df_natrolls.shape[1]+1):
        df3[f'modtotal_{i}'] = pd.to_numeric(df3[f'totalroll_{i}']) - pd.to_numeric(df3[f'natroll_{i}'])

    return df3



split_df= split_roll_data(df)
#print(split_df.head())

# specify the file name to save
save_type = [('CSV Files', '*.csv')]
roll_file_name = "Rol20RollTotalsSplit.csv"

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# check if the file exists in the working directory
if os.path.isfile(roll_file_name):
    # if the file exists, save the dataframe to it
    split_df.to_csv(roll_file_name, index=False)
else:
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # hide the root window

    # display the file dialog to select a save location and name
    file_path = filedialog.asksaveasfilename(initialfile=roll_file_name, filetypes=save_type)

    # check if a file was selected and save the dataframe if so
    if file_path:
        split_df.to_csv(file_path, index=False)

