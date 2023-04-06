import csv
import tkinter as tk
from tkinter import filedialog
import chardet
from bs4 import BeautifulSoup
import requests
import html5lib
import lxml
import sys
sys.setrecursionlimit(2000)
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd
import sqlite3
import pathlib
import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import os
import re
import re
import math
from numpy import nan

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)


# specify the file name to import
raw_json = "chat_archive.json"

# Detect the encoding of the file
def import_json(file_path):
    # Open the file as plain text
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read the file contents
        file_contents = f.read()

    # Attempt to parse the JSON data
    try:
        data = json.loads(file_contents)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {str(e)}")
        return None

    return data

# check if the file exists in the working directory
if os.path.isfile(raw_json):
    # if the file exists, import it using pd.read_csv
    file_path=raw_json
    df = pd.DataFrame(import_json(file_path))
else:
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog window for selecting the JSON file
    file_path = filedialog.askopenfilename(filetypes=[('json Files', '*.json')])
    df = pd.DataFrame(import_json(file_path))


data = df

file_size = os.path.getsize(file_path)
print(f"Json file size: {file_size} bytes")
    
#num_lines = len(data)
#print("number of lines")
#print(num_lines)

#recursive searchs
import json
import os
import re

def find_roll(data):
    inlinerolls = data.get('inlinerolls', [])
    roll_data = []
    for inlineroll in inlinerolls:
        expression = inlineroll.get('expression', '')
        results = inlineroll.get('results', {})
        rolls = results.get('rolls', [])
        total = results.get('total', 0)
        modifier = ""
        expr_str = ''
        roll_value = 0
        if not rolls:
            rolls = [{}]
        for expr_item in rolls:
            if expr_item.get('type', '') == 'M':
                expr_str += str(expr_item.get('expr', ''))
                modifier += str(expr_item.get('expr', ''))
            elif expr_item.get('type', '') == 'L':
                expr_str += expr_item.get('text', '')
            elif expr_item.get('type', '') == 'R':
                roll_value += expr_item.get('results', [{}])[0].get('v', 0)
        roll_data.append({
            'expression': expression,
            'result': roll_value,
            'modifier': modifier,
            'expr': expr_str,
            'total': total
        })
    return roll_data












def find_info(data):
    info = {'rname': None, 'charname': None, 'name': None, 'rolls': []}
    rname_found = False
    if isinstance(data, str):
        return None, False
    for key, value in data.items():
        if isinstance(value, dict) and "content" in value:
            content = value["content"]
            if isinstance(content, str):
                match = re.search(r"{rname=.*?[}\]]", content)
                if match:
                    rname = re.sub(r'[=]\^?\{??|\[|\-u', '', match.group()[7:-1])
                    info['rname'] = rname
                    rname_found = True
                
                charname = None
                name = None
                substrings = re.split(r"}{", content)
                for substring in substrings:
                    char_match = re.search(r"(?:{{charname=|{charname=|charname=)([^{}[\]]*)(?:}}|\"|$|\s)", substring)
                    name_match = re.search(r"(?:{{name=|{name=|name=)((?:\w+\s?|[^\{\}\[\]]|\[[^\[\]]*\]|{\w+}|-\w|\([^\)]*\))+?)(?:}}|\"|$|\s)", substring)
                    if char_match:
                        charname = re.sub(r'\^?\{??|\[|\-u', '', char_match.group(1)).strip()
                    if name_match:
                        name = re.sub(r'\^?\{??|\[|\-u', '', name_match.group(1)).strip()
                    if charname and name:
                        break
                
                info['charname'] = charname
                info['name'] = name
                
                # print combined entries 
                #try:
                #    roll_data = find_roll(content)
                #    if roll_data:
                #        info['rolls'].append(roll_data)
                #        print(info)
                #except Exception as e:
                    #print(f"Error while processing content: {content}")
                    #print(f"Exception message: {str(e)}")
                    
                #call find_roll
                if isinstance(value, dict):
                    roll_data = find_roll(value)
                else:
                    roll_data = find_roll(content)
                if roll_data:
                    info['rolls'].append(roll_data)

                if all(info.values()):
                    return key, info, rname_found
            else:
                sub_key, sub_info, sub_rname_found = find_info(content)
                if sub_info:
                    info['rolls'].append(sub_info['rolls'])
                    del sub_info['rolls']
                    info.update(sub_info)
                    return key, info, sub_rname_found

        elif isinstance(value, dict):
            sub_key, sub_info, sub_rname_found = find_info(value)
            if sub_info:
                info['rolls'].append(sub_info['rolls'])
                del sub_info['rolls']
                info.update(sub_info)
                return key, info, sub_rname_found
  
    #if info.get('rname') is not None:
        #print(info)

    
    return None, False, False




# Search for "{rname=" in all values
results = []

if isinstance(data, list):
    for obj in data:
        result_key, result_info, result_rname_found = find_info(obj)
        if result_info and result_rname_found:
            key = result_key
            info = result_info
            
            rolls = info.pop('rolls', []) # Extract 'rolls' key from 'info' dictionary

            for roll_data in rolls:
                expression_list = []
                result_list = []
                expr_list = []
                total_list = []
                
                for roll in roll_data:
                    expression_list.append(roll['expression'])
                    result_list.append(roll['result'])
                    expr_list.append(roll['expr'])
                    total_list.append(roll['total'])
                
                # Append the new columns to the 'info' dictionary
                info['expression'] = expression_list
                info['result'] = result_list
                info['expr'] = expr_list
                info['total'] = total_list
                
                obj.update(info)  # Update original dictionary with new columns and values
                results.append({"key": key.lstrip('-='), "rname": info['rname'].lstrip('^{['), "charname": info['charname'], "expression": expression_list, "result": result_list, "expr": expr_list, "total": total_list})

else:
    for key, value in data.items():
        result_key, result_info, result_rname_found = find_info(value)
        if result_info and result_rname_found:
            info = result_info

            rolls = info.pop('rolls', []) # Extract 'rolls' key from 'info' dictionary

            for roll_data in rolls:
                expression_list = []
                result_list = []
                expr_list = []
                total_list = []

                for roll in roll_data:
                    expression_list.append(roll['expression'])
                    result_list.append(roll['result'])
                    expr_list.append(roll['expr'])
                    total_list.append(roll['total'])

                # Append the new columns to the 'info' dictionary
                info['expression'] = expression_list
                info['result'] = result_list
                info['expr'] = expr_list
                info['total'] = total_list
                
                value.update(info)  # Update original dictionary with new columns and values
                results.append({"key": key.lstrip('-='), "rname": info['rname'].lstrip('^{['), "charname": info['charname'], "expression": expression_list, "result": result_list, "expr": expr_list, "total": total_list})



print("Number of results:", len(results))

df = pd.DataFrame(results)

###Edit DataFrame Entries

# print and save results to csv
#print(df.head())
#print(df.tail())


# specify the file name to save
save_type = [('CSV Files', '*.csv')]
initial_file_name = "Roll20InitialJsonToDF.csv"

# get the directory where the launch script is located
launch_dir = os.path.dirname(os.path.abspath(__file__))

# change the working directory to the launch directory
os.chdir(launch_dir)

# check if the file exists in the working directory
if os.path.isfile(initial_file_name):
    # if the file exists, save the dataframe to it
    df.to_csv(initial_file_name, index=False)
else:
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # hide the root window

    # display the file dialog to select a save location and name
    file_path = filedialog.asksaveasfilename(initialfile=initial_file_name, filetypes=save_type)

    # check if a file was selected and save the dataframe if so
    if file_path:
        df.to_csv(file_path, index=False)