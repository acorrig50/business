import requests
from bs4 import BeautifulSoup
import re
import numpy as np

# _____About_____
# Class to house the methods necessary for the ebay bot to operate
# Currently under maintenance
class Starkiller():
    
    # _____Use_____
    # 1. This method takes in user input, splits the input and rejoins it so that the url will understand what the search is for
    # 2. Later on, I will take the page that the URL returns and scrape it for needed information
    # 3. It then searches the URL and finds the elements given to the BeautifulSoup object 
    def input_price_recon(self):
        
        clothing_type = input("Please enter the item you wish to search: ")
        clothing_type = clothing_type.split(' ')
        clothing_type = '+'.join(clothing_type)
        print("Your search is for: {}".format(clothing_type))
        

        url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=" + clothing_type + "&_sacat=0&LH_TitleDesc=0&_odkw=" + clothing_type + "&_osacat=0")

        print(url)
        
        soup = BeautifulSoup(url.content, 'html.parser')
        
        # Looping through and stripping the element will be the only way it seems.
        # and by looping, I mean a buncha loops lol sorry future me but it works
        main_content = soup.find_all(attrs={'class':'s-item__price'})
        prices_list = []
        for each in main_content:
            prices_list.append(each.get_text())
        clean_prices = []
        for price in prices_list:
            new_price = price.strip("$,")
            newer_price = new_price.split(' ')
            clean_prices.append(newer_price)
        cleanest_prices = []
        for price_set in clean_prices:
            for price in price_set:
                newest_price = price.strip("$")
                even_newer = newest_price.strip('to')
                cleanest_prices.append(even_newer)
        true_prices = []
        for price in cleanest_prices:
            if price == '':
                continue
            else:
                stripped_true = price.strip(",")
                true_prices.append(float(stripped_true))
        
       
        # This block can be used for larger numbers that involve commas
        """this_is_it_im_serious = []
        for price in true_prices:
            true_price = price.strip('[1-9],')
            print(true_price) 
            this_is_it_im_serious.append(float(true_price))
        print(this_is_it_im_serious)
        """
        
        # Printing out the stats of the first page scraped
        average_price = np.average(true_prices)
        min_price = np.min(true_prices)
        max_price = np.max(true_prices)
        print("The average price for this item is: {}".format(average_price))
        print("The minimum price for this item is: {}".format(min_price))
        print("The maximum price for this item is: {}".format(max_price))
        
    # _____Use_____
    # 1. This method finds the prices of each item and puts them into a list to be averaged out
    #    The averages can then be used to decide what price an item should be listed at 
    def file_price_scraper(self):
        
        # Creating a list, then opening a file to feed the list its contents
        clothes_list = []
        with open('scraping\input.txt', 'r') as file:
            clothes_list.append(file.read())
        
        # Turning the list into a string for modification, then return it BACK to
        # list form to be used by the for loop holding the URL
        to_string = ""
        for word in clothes_list:
            for letter in word:
                to_string += letter

        to_string = to_string.split("\n")

        # Establish a list of URL's that we will then take and use b4 on 
        url_list = []    
        for i in range(len(to_string)):
            url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=" + to_string[i] + "&_sacat=0&LH_TitleDesc=0&_odkw=" + to_string[i] + "&_osacat=0")
            url_list.append(url)   
            
        # Now we loop throught the URL's and gather the info we need on each item.
        # This code below will get the inner text of the price and clean it so that it can be put
        #   into a list. Once it is in list form, we will then append this to the item_prices list
        #   so that it can be split and deciphered into metrics to better understand the item
        item_prices = []
        for url in url_list:
            soup = BeautifulSoup(url.content, 'html.parser')
            
            main_content = soup.find_all(attrs={'class':'s-item__price'})
            prices_list = []
            for each in main_content:
                prices_list.append(each.get_text())
            clean_prices = []
            for price in prices_list:
                new_price = price.strip("$,")
                newer_price = new_price.split(' ')
                clean_prices.append(newer_price)
            cleanest_prices = []
            for price_set in clean_prices:
                for price in price_set:
                    newest_price = price.strip("$")
                    even_newer = newest_price.strip('to')
                    cleanest_prices.append(even_newer)
            true_prices = []
            for price in cleanest_prices:
                if price == '':
                    continue
                else:
                    stripped_true = price.strip(",")
                    true_prices.append(float(stripped_true))
                    
            item_prices.append(true_prices)
        
        # Calculating metrics based on each list within the item_prices list
        for i in range(len(item_prices)):
            print("________________Stats for {}________________".format(to_string[i]))
            print("Average price of item: {}".format(np.average(item_prices[i])))
            print("Maximum price of item: {}".format(np.max(item_prices[i])))
            print("Minimum price of item: {}".format(np.min(item_prices[i])))
    
    # _____Use_____
    # 1. Does the same process as file_price_scraper, but the ULR has been set to be True for Buy It Now. 
    #    This means that the only prices that will be gathered for analysis are the items with the buy it now tag.
    def file_price_scraper_bin(self):
        # Creating a list, then opening a file to feed the list its contents
        clothes_list = []
        with open('modules\input_clothes.txt', 'r') as file:
            clothes_list.append(file.read())
        
        # Turning the list into a string for modification, then return it BACK to
        # list form to be used by the for loop holding the URL
        to_string = ""
        for word in clothes_list:
            for letter in word:
                to_string += letter

        to_string = to_string.split("\n")

        # Establish a list of URL's that we will then take and use b4 on 
        url_list = []    
        for i in range(len(to_string)):
            url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=" 
                               + to_string[i] + "&_sacat=0&LH_TitleDesc=0&LH_BIN=1&LH_Sold=1&LH_ItemCondition=4&rt=nc")
            url_list.append(url)   
            
        # Now we loop throught the URL's and gather the info we need on each item.
        # This code below will get the inner text of the price and clean it so that it can be put
        #   into a list. Once it is in list form, we will then append this to the item_prices list
        #   so that it can be split and deciphered into metrics to better understand the item
        item_prices = []
        for url in url_list:
            soup = BeautifulSoup(url.content, 'html.parser')
            
            main_content = soup.find_all(attrs={'class':'s-item__price'})
            prices_list = []
            
            # These loops below are strictly used to clean the prices_list for use
            for each in main_content:
                prices_list.append(each.get_text())
            clean_prices = []
            for price in prices_list:
                new_price = price.strip("$,")
                newer_price = new_price.split(' ')
                clean_prices.append(newer_price)
            cleanest_prices = []
            for price_set in clean_prices:
                for price in price_set:
                    newest_price = price.strip("$")
                    even_newer = newest_price.strip('to')
                    cleanest_prices.append(even_newer)
            true_prices = []
            for price in cleanest_prices:
                if price == '':
                    continue
                else:
                    stripped_true = price.strip(",")
                    true_prices.append(float(stripped_true))
                    
            item_prices.append(true_prices)
        
        # Calculating metrics based on each list within the item_prices list
        print("The following are stats for buy it now products")
        for i in range(len(item_prices)):
            print("________________Stats for {}________________".format(to_string[i]))
            print("Average price of item: {}".format(np.average(item_prices[i])))
            print("Maximum price of item: {}".format(np.max(item_prices[i])))
            print("Minimum price of item: {}".format(np.min(item_prices[i])))
      
    
    # _____Use_____
    # NOTE: alt version of chance_to_sell, going to try and simplify the method and 
    #   reimplement in a different way, someday
    # A function that finds the total number of listings that match our item and divides the number
    # of items that are sold by the total number listed, giving us the sellthrough percentage
    def chance_to_sell(self):
        # Creating a list, then opening a file to feed the list its contents
        clothes_list = []
        with open('modules\input_clothes.txt', 'r') as file:
            clothes_list.append(file.read())
        
        # Turning the list into a string for modification, then return it BACK to
        # list form to be used by the for loop holding the URL
        to_string = ""
        for word in clothes_list:
            for letter in word:
                to_string += letter

        to_string = to_string.split("\n")

        # Establish a list of URL's and sold URL's to get the number of total listings from the 
        # default URL page and the total number sold from the sold URL page
        url_list = []
        sold_url_list = []    
        for item in to_string:
            url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=" 
                                + item + "&_sacat=0&LH_TitleDesc=0&LH_BIN=1&LH_ItemCondition=4&rt=nc&_fsrp=1")
            url_list.append(url)   
            
        for item in to_string:
            url = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw="
                                + item +" &_sacat=0&LH_TitleDesc=0&LH_BIN=1&LH_ItemCondition=4&_fsrp=1&rt=nc&LH_Sold=1&LH_Complete=1")
            sold_url_list.append(url)
        
        # _____Grabbing for listed totals______
        # Now we want to grab the total number of items sold for each item in OUR list
        listed_amounts = []
        for url in url_list:
            soup = BeautifulSoup(url.content, 'html.parser')
            main_content = soup.find_all(attrs={'class':'srp-controls__count-heading'})
            
            for element in main_content:
                    listed_amounts.append(element.get_text())
            
        
        # _____Grabbing for sold totals______
        # Now we want to grab the total number of items SOLD for each item in OUR list
        sold_amounts = []
        for url in sold_url_list:
            soup = BeautifulSoup(url.content, 'html.parser')
            main_content = soup.find_all(attrs={'class':'srp-controls__count-heading'})
            
            for element in main_content:
                    sold_amounts.append(element.get_text())
        
        # Splitting the lists 'listed_amounts' and 'sold_amounts'
        listed_amounts_split = []
        for element in listed_amounts:
            listed_amounts_split.append(element.split(' '))
        
        sold_amounts_split = []
        for element in sold_amounts:
            sold_amounts_split.append(element.split(' '))
        
        # Now that we have both lists split and appended to a new list, we can now take the first
        #   element of each inner list, meaning we will have the total amount of listed items for 
        #   our searched item
        
        # _____Listed amounts loop_____
        total_amounts_listed = []
        cleaned_listed_amounts = []
        for list in listed_amounts_split:
            for inner_element in list:
                inner_element = inner_element.replace(',', '').replace('+','')
                cleaned_listed_amounts.append(inner_element)


        # _____Sold amounts loop_____
        total_amounts_sold = []
        cleaned_sold_amounts = []
        for list in sold_amounts_split:
            for inner_element in list:
                inner_element = inner_element.replace(',', '').replace('+','')
                cleaned_sold_amounts.append(inner_element)
        
        
        # IMPORTANT NOTE: Now that both lists and their elements are cleaned of commans 
        #   plus signs, we need to grab only the numbers from the cleaned lists and
        #   if it is a number, then we append it to the total_amounts_listed and 
        #   total_amounts_sold 
        for element in cleaned_listed_amounts:
            if element.isdigit():
                total_amounts_listed.append(int(element))
            
        for element in cleaned_sold_amounts:
            if element.isdigit():
                total_amounts_sold.append(int(element))
        
        
        
        # Now we perform calculations and print them out for each item
        # NOTE: Where I left off
        for i in range(len(to_string)):
            print("_____{}_____".format(to_string[i]))
            print("Amount listed: {} / Amount sold: {}".format(total_amounts_listed[i],total_amounts_sold[i]))
            print("Turnover rate: {}".format(round(total_amounts_sold[i] / total_amounts_listed[i], 2)))
        
    # _____Use_____
    # NOTE: Under construction
    # Current plans are to have this function take in the details from the webpage that details items sold and make a dataframe
    # of those items, allowing for quick analysis of trends in items sold 
    def create_dataframe(self):
        pass   

star = Starkiller()
# Uncomment this back to see the average prices, otherwise you'll get turnover rate only
# star.file_price_scraper_bin()
star.chance_to_sell()











