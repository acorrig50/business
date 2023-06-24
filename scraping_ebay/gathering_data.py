import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# Establishing the URL needed for scraping
url = 'https://www.ebay.com/b/Tops-Blouses-Size-XS-for-Women/53159/bn_52462765?LH_BIN=1&rt=nc&_udlo=35&mag=1'       # URL that searches for womens tops over $35
url2 = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&rt=nc&LH_Sold=1&LH_Complete=1&_pgn=2'     # Second page of URL that searches for womens jeans above $35
url3 = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&rt=nc&LH_BIN=1&_pgn=2'       # Same as second URL but items are not 'completed' so no best offers are included and auctions are exluded
big_page_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&LH_BIN=1&rt=nc&_ipg=240&_pgn=1'

# Establish a list of Big URLs to gather data from
# NOTE: I'm leaving this note to designate this as the original version, going to make another file to try looping through the url list to gather data much more data
big_url_list = []
for i in range(1,42):
    big_url_list.append('https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&LH_BIN=1&rt=nc&_ipg=240&_pgn={}'.format(i))

# HTML tags and other necessary details
# class="s-item__title--tag"        # contains the date the item was sold
# class="s-item__title"             # contains the name of the item
# class="SECONDARY_INFO"            # contains the condition (preowned/brandnew) of the item
# class="s-item__price"             # contains the price of the item


# Coding below
r = requests.get(big_page_url)
webpage = r.content
soup = BeautifulSoup(webpage, 'html.parser')

# Looking for the name of each item on the page
listed_elements = soup.find_all(attrs={
    'class': 's-item__title'
})

item_names = soup.find_all(attrs={
    'role': 'heading'
})

dates_sold = soup.find_all(attrs={
    'class': 'POSITIVE',
})

print("There are {} items listed".format(len(listed_elements)))  # Find out how many items are listed on the page

# Getting the names for each item
names = []
for name in item_names: # Print the names
    if 'Shop on Ebay' in name:
        continue
    names.append(name.get_text())   # Appending the text retrieved from html tag to a list for analysis later on

print("________________________________________________________________")
    
# Getting the date sold for each item
date_sold_and_price_sold_for = []
for element in dates_sold:
    date_sold_and_price_sold_for.append(element.get_text()) # Grabbing the first element, which is the date, from the dictionary and appending it to a list

# Now that we have the elements in a list, we can take the even elements, which are the dates, and odd elements, which are the prices
dates = []
prices = []
for i in range(len(date_sold_and_price_sold_for)):
    if 'Sold' in date_sold_and_price_sold_for[i]:
        dates.append(date_sold_and_price_sold_for[i])
    if '$' in date_sold_and_price_sold_for[i]:
        prices.append(date_sold_and_price_sold_for[i])
 # Take away the first element in the names list because it is not needed


# Now we have the lists established for the first page, lets turn it into a dataframe
data = {
    'item_name': names,
    'item_price': prices,
    'date_sold':dates
}

# For some reason, the prices are not the same length, so we need to fix that here
names.pop(0)

# Creating and displaying the frame
df = pd.DataFrame(data)
print(df.head())
print(df.info())

# Stripping the dollar sign from item_price and changing its type to float
df['item_price'] = df['item_price'].apply(lambda x: x.strip('$'))
df = df.astype({'item_price': 'float'})

# Sorting by highest price
highest_price = df.sort_values(by='item_price', ascending=False)
lowest_price = df.sort_values(by='item_price', ascending=True)

# Exporting to excel file
df.to_excel(r'scraping\project_godstar\excel_sheet.xlsx', index=False)