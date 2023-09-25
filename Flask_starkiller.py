import requests
from bs4 import BeautifulSoup
import re
import numpy as np


# _____About_____
# Class to house the methods necessary for the ebay bot to operate
# Currently under maintenance
class Starkiller():
    # _____Use_____
    # NOTE: alt version of chance_to_sell, going to try and simplify the method and 
    #   reimplement in a different way, someday
    # A function that finds the total number of listings that match our item and divides the number
    # of items that are sold by the total number listed, giving us the sellthrough percentage
    def chance_to_sell(self, searched_item):
        # Establish a list of URL's and sold URL's to get the number of total listings from the 
        # default URL page and the total number sold from the sold URL page
      
        to_string_item_name = str(searched_item)
        
        listed_url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + to_string_item_name + "&_sacat=0")   

        sold_url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + to_string_item_name + "&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1")
        
        # _____Grabbing for listed totals______
        # Now we want to grab the total number of items sold for each item in OUR list
        soup = BeautifulSoup(listed_url.content, 'html.parser')
        listed_number = soup.find_all(attrs={'class':'srp-controls__count-heading'})
        
            
        # _____Grabbing for sold totals______
        # Now we want to grab the total number of items SOLD for each item in OUR list
        soup = BeautifulSoup(sold_url.content, 'html.parser')
        sold_number = soup.find_all(attrs={'class':'srp-controls__count-heading'})
        
        #Assign the lists to a var, then split the lists based on spaces
        listed_split = listed_number[0].get_text().split(' ')
        sold_split = sold_number[0].get_text().split(' ')
        
        # Taking the first item from the list, which are the numbers we wanted. Then we turn them to integers
        listed_total = listed_split[0].strip('+').replace(',', '')
        sold_total = sold_split[0]
        numb_listed = int(listed_total)
        numb_sold = int(sold_total)
        
        return round((numb_sold / numb_listed), 3)
        
        

            

        
        
        










