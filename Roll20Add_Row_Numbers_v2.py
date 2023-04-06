import os
import csv
from collections import defaultdict

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# Path to directory containing CSV files
csv_dir1 = "character_output/"
# Path to directory containing CSV files
csv_dir2 = "roll_output/"

def add_roll_count(csv_dir1, csv_dir2):
    for csv_dir in [csv_dir1, csv_dir2]:
        # Loop over each CSV file in the directory
        for filename in os.listdir(csv_dir):
            if filename.endswith(".csv"):
                filepath = os.path.join(csv_dir, filename)

                # Read in the CSV file
                with open(filepath, "r") as f:
                    reader = csv.reader(f)
                    rows = list(reader)

                # Check if the CSV file already has a "RollCount" column
                if "RollCount" in rows[0]:
                    print(f"Skipping {filename}: already has a RollCount column")
                    continue
                
                # Add a new column to each row, starting from the second row
                # and a new column to count the number of rows for each unique "charname" value
                char_count = defaultdict(int)
                for i, row in enumerate(rows[1:], start=1):
                    charname = row[1]
                    char_count[charname] += 1
                    row.insert(0, i)
                    row.insert(1, char_count[charname])
                
                # Add the new column headers to the first row
                rows[0].insert(0, "RollCount")
                rows[0].insert(1, "PlayerRollCount")
                
                # Write the modified rows back to the CSV file
                with open(filepath, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(rows)

add_roll_count(csv_dir1,csv_dir2)