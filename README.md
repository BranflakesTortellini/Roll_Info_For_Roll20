# Roll20JsonToStatsProcessor
Takes json files pulled from Roll20 and extracts the roll data into a dataframe and csv for easy statistical analysis. 

Use the Roll20Exporter chrome extension to pull json files from Roll20 and the run these scripts using the chatarchive file.

https://chrome.google.com/webstore/detail/r20exporter/apbhfinbjilbkljgcnjjagecnciphnoi?hl=en

Credit to:https://github.com/kakaroto/R20Exporter/

Put all of the scripts and the archive in the same folder and run the launch script.

Features: 
1) CSV files for rolls by action type, die type and character name. 

2) Overall summary file which includes count, mean, median, mode and std for characters selected by the user from a drop down.

3) Roll counter for overall rolls and rolls per player specific to an action. You can basically create a time series plot of a player's success over time for a specific action type, die type, etc. 

4) Added a "luck" measurement to easily see if a player is rolling above or below what they're expected to roll. Over enough rolls this should be ~0.5 average so if a player is higher or lower than that over a long period of time then you know if they are lucky or not.

5) Automatic calculation of statistical average for die type. 

6) Optional name fixer which allows one to edit the names or players or actions which had a typo or were changed at somepoint during the campaign to help keep the data consistent. Similarly the GM could highlight all NPCs and change their name to GM. 


Works in progress:

1)Dashboard to display data with various stats

2)Expanded functionality to analyze compound rolls or non-standard rolls, largely involves spell/weapon attack rolls especially with custom modifiers

3)Creation of summary files by roll, player, die including various quick reference information like mean/median/mode/std of individuals or groups

4)Automatic differentiation between npcs and pcs. 

5)Remote hosting/login capability for dashboard


A dashboard is planned to make it easier to display said stats.

List of packages required for operation:
 csv
 
 bs4 
 
 chardet
 
 collections 
 
 html5lib
 
 json
 
 jsonpath_ng
 
 lxml
 
 math
 
 numpy  
 
 os
 
 pandas 
 
 pathlib
 
 re
 
 requests
 
 sqlite3
 
 string
 
 sys
 
 tkinter  
 
 unicodedata

Install packages with: pip install csv bs4 chardet ollections tml5lib json jsonpath_ng lxml math numpy pandas pathlib requests sqlite3 string tkinter unicodedata
