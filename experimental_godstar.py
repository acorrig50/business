import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# Establishing the URL needed for scraping
url3 = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&rt=nc&LH_BIN=1&_pgn=2'       # Same as second URL but items are not 'completed' so no best offers are included and auctions are exluded
big_page_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&LH_BIN=1&rt=nc&_ipg=240&_pgn=1'
regular_size_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&LH_BIN=1&LH_Sold=1&rt=nc&_udlo=35&_ipg=60&_pgn=1'

# Establish a list of Big URLs to gather data from
big_url_list = []
regular_url_list = []
# NOTE: Change the params back to 1-30 after limit testing
for i in range(1,25):
    big_url_list.append('https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&LH_BIN=1&rt=nc&_ipg=240&_pgn={}'.format(i))
    regular_url_list.append('https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&LH_BIN=1&LH_Sold=1&rt=nc&_udlo=35&_ipg=60&_pgn={}'.format(i))


# HTML tags and other necessary details
# class="s-item__title--tag"        # contains the date the item was sold
# class="s-item__title"             # contains the name of the item
# class="SECONDARY_INFO"            # contains the condition (preowned/brandnew) of the item
# class="s-item__price"             # contains the price of the item


names = []
dates = []
prices = []
conditions = []
# NOTE: Change regular_url_list back to big_url_list if it doesnt work properly
for url in regular_url_list:
    # Coding below
    r = requests.get(url)
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
        'class': 'POSITIVE'
    })
    
    prices_sold = soup.find_all(attrs={
        'class': 's-item__price'  
    })
    
    other_dates_sold = soup.find_all(attrs={
        'class': 's-item__title--tag'
    })
    
 
    
    # Getting the names for each item
    for name in item_names: 
        if 'Shop on Ebay' in name:
            continue
        names.append(name.get_text())   # Appending the text retrieved from html tag to a list for analysis later on
        
    # Getting price for each item on the page
    for price in prices_sold:
        prices.append(price.get_text())

    # Getting the date for each item on the page                
    for date in other_dates_sold:
        dates.append(date.get_text())
     
    # Getting the condition for each item on the page 
    # NOTE: THIS LINE BREAKS EVERYTHING WHY IDK
    """for status in condition:
        condition.append(status)"""
        
    names.pop(0) 
    prices.pop(0)
    print(len(names))
    print(len(prices))
    print(len(dates))


# Now we have the lists established for the first page, lets turn it into a dataframe
data = {
    'item_name': names,
    'item_price': prices,
    'date_sold': dates
}

# Creating and displaying the frame
df = pd.DataFrame(data)
print(df.info())

# Stripping the dollar sign from item_price and changing its type to float
df['item_price'] = df['item_price'].apply(lambda x: x.strip('$'))
df = df.astype({'item_price': 'float'})

print(df.info())
print(df.to_string()) 




