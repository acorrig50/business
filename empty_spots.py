# NOTE: To use, take most recent version of revised_locations, copy into this folder and then run the code. The final sheet
#   will load on the outtermost folder
import pandas as pd
import numpy as np


inv_sheet = pd.read_excel(r"C:\Users\alexc\Documents\Visual Studio\file_tools\revised_locations.xlsx")

print(inv_sheet.info())

# Replace all the "nan" values with 0's in order to better identify them
#   when looping through the frame
inv_sheet['name'] = inv_sheet['name'].fillna(0)

# Create list to store the sku's in that are empty
empty_skus = []

# Loop through the frame with a surface loop and find the empty names, then
#   add the skus in the name to the list
for i in inv_sheet.index:
    if inv_sheet['name'][i] == 0:
        empty_skus.append(inv_sheet['bin'][i])
       
# Make a list to count as the index
index_list = [i + 1 for i in range(len(inv_sheet['bin']))]

# Merge the two lists together into a dict to make a frame
new_df = pd.DataFrame(list(zip(index_list, empty_skus)), columns= ['index','sku'])

# Turn df into excel sheet, use excel sheet to fill in empty inv spots!
new_df.to_excel('new_empty spots.xlsx')

# NOTE READ ME: Made change to line 21 and added an or statement, erase if non-functional