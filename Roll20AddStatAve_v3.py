import os
import csv
from collections import defaultdict
from collections import Counter

import re

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# Path to directory containing CSV files
csv_dir1 = os.getcwd()



def Add_Statistical_Average(csv_dir1):
    for csv_dir in [csv_dir1]:
        for file in os.listdir(csv_dir):
            if file.endswith('.csv'):
                filename = os.path.join(csv_dir, file)
                with open(filename, 'r', newline='') as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    data = [row for row in reader]

                # get the index of the expression column
                expr_index = headers.index('expression')

                # get a list of unique xdy structures and their corresponding stat averages
                xdy_stats = {}
                for row in data:
                    expr = row[expr_index]
                    match = re.search(r'\b(\d+d\d+)(?=[^\d]|$)', expr)
                    if match:
                        xdy = match.group(1)
                        x, y = map(int, xdy.split('d'))
                        stat_ave = (((y+1)/2) * x)
                        xdy_stats[xdy] = stat_ave

                # get the most common stat average in the sheet
                mode_statave = Counter([row[-1] for row in data]).most_common(1)[0][0]

                # add the stat average and die type columns to the headers and data
                stat_ave_header = 'StatAve'
                die_type_header = 'DieType'
                headers.insert(headers.index('total')+1, stat_ave_header)
                headers.insert(headers.index(stat_ave_header)+1, die_type_header)
                for row in data:
                    expr = row[expr_index]
                    match = re.search(r'\b(\d+d\d+)(?=[^\d]|$)', expr)
                    if match:
                        xdy = match.group(1)
                        die_type = xdy
                        row.insert(headers.index('total')+1, xdy_stats.get(xdy))
                        row.insert(headers.index(stat_ave_header)+1, die_type)
                    else:
                        row.insert(headers.index('total')+1, mode_statave)
                        row.insert(headers.index(stat_ave_header)+1, '')

                # write the updated data to the file
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(data)


                    
Add_Statistical_Average(csv_dir1)