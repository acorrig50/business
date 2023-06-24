import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# Establishing the URL needed for scraping
url3 = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&rt=nc&LH_BIN=1&_pgn=2'       # Same as second URL but items are not 'completed' so no best offers are included and auctions are exluded
big_page_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&_udlo=25&LH_Sold=1&LH_BIN=1&rt=nc&_ipg=240&_pgn=1'
regular_size_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&LH_BIN=1&LH_Sold=1&rt=nc&_udlo=35&_ipg=60&_pgn=1'
regular_size_url_preowned = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=womens+jeans&_sacat=0&LH_BIN=1&LH_Sold=1&_udlo=30&rt=nc&LH_ItemCondition=3000&_pgn=1'

    
def gather_stats(url_string):
    
    # Establish a list of Big URLs to gather data from
    big_url_list = []
    regular_url_list = []
    
    # NOTE: Change the loop length to change the number of pages scraped, higher number = better sample size
    for i in range(1,80):
        big_url_list.append('https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_udlo=25&LH_Sold=1&LH_BIN=1&rt=nc&_ipg=240&_pgn={}'.format(url_string, i))
        regular_url_list.append('https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&LH_BIN=1&LH_Sold=1&rt=nc&_udlo=35&_ipg=60&_pgn={}'.format(url_string, i))
    
    # Establish lists that we will store different facets of data for each item on eBay 
    names = []
    dates = []
    prices = []
    conditions = []
    pictures = []
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
        
        item_conditions = soup.find_all(attrs={
            'class': 'SECONDARY_INFO'
        })
        
        pictures_dict = soup.find_all(attrs={
            'img'
        })
        
        
        
        #__UNDER CONSTRUCTION____________________________
    
        img_tags = soup.find_all('img')
        response = requests.get(url)
        images = [img['src'] for img in img_tags]


        for url in images:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
            if not filename:
                print("Regex didn't match with the url: {}".format(url))
                continue
            with open(filename.group(1), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative 
                    # if it is provide the base url which also happens 
                    # to be the site variable atm. 
                    url = '{}'.format( url)
                response = requests.get(url)
                f.write(response.content)
        
        
        
        
        
        
        #__CONSTRUCTION ZONE ENDS_______________________________
        
        
        
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
            
        # Getting the condition for each item and appending it to a list
        for condition in item_conditions:
            conditions.append(condition.get_text())
            
        
        # Getting the condition for each item on the page 
        # NOTE: THIS LINE BREAKS EVERYTHING WHY IDK
        """for status in condition:
            condition.append(status)"""
            
        names.pop(0) 
        prices.pop(0)
        conditions.pop(0)

        print(len(names))
        print(len(prices))
        print(len(dates))
        print(len(conditions))
        print(pictures)
        print("..........")
        
    # Now we have the lists established for the first page, lets turn it into a dataframe
    data = {
        'item_name': names,
        'item_price': prices,
        'date_sold': dates,
        # Taking conditions away while searching in mens department, seems to be breaking 
        'item_condition': conditions
    }

    # Creating and displaying the frame
    df = pd.DataFrame(data)
    print(df.info())


    # Need to figure out how to strip the dollar sign AND the second number from the entries that have 2 numbers
    # Stripping the dollar sign from item_price and changing its type to float
    df['item_price'] = df['item_price'].apply(lambda x: x.strip('$'))
    #df = df.astype({'item_price': 'float'}) // Can't run this line because of the double price listings

    # Setting item names to all lowercase
    df['item_name'] =  df['item_name'].apply(lambda x: x.lower())
    df['date_sold'] = df['date_sold'].apply(lambda x: 'Today' if 'Jun' in x else 'Not today')


    # Creating a list to count each time high rise and boot cut occur within the names of the frame, could also just make a column that 
    # contains 0 or 1 for each time high rise and/or boot cut is in the name!
    # NOTE: can delete if the column creation code below is successful
    high_rise_count = [1 for i in df['item_name'] if  'high' in df['item_name']]  
    boot_count = [1 for i in df['item_name'] if 'boot' in df['item_name']]  

    # Turning the frame into an excel file
    df.to_excel('{}.xlsx'.format(url_string))
    
    
# Run the main method with your category and specifications as the parameter, get a excel sheet back as output
gather_stats('womens jeans')
    

