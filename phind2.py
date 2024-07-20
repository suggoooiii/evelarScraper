import cloudscraper
from bs4 import BeautifulSoup
import re
import json
import logging
import os
# Create a scraper instance
scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

url = "https://www.101evler.com/north-cyprus/houses-to-rent?page=1"



def load_existing_listings():
    try:
        if os.path.exists('listings.json'):
            with open('listings.json', 'r', encoding='utf-8') as f:
                all_listings = json.load(f)
                print(f'all_listings: {all_listings}')
                return json.load(f)
        return []
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from listings.json. Starting with an empty list.")
        return []


load_existing_listings()
# try:
#     # Get the page content
#     response = scraper.get(url)
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Find all h4 elements with class starting with "text-block-"
#         h4_elements = soup.find_all('h4', class_=re.compile(r'^text-block-'))
        
#         # Find all div elements with class "basicprice"
#         price_elements = soup.find_all('div', class_='basicprice')
        
#         # Read existing listings
#         existing_listings = []
#         if os.path.exists('listings.json'):
#             with open('listings.json', 'r', encoding='utf-8') as f:
#                 for line in f:
#                     listing = json.loads(line)
#                     print(f'listing: {listing}')
#                     # all_listings.append(listing)
        
        
#         # Extract information from each listing
#         # for h4, price in zip(h4_elements, price_elements):
#         #     # print(f'h4: {h4} price: {price}')
#         #     title = h4.text.strip()
#         #     price_value = price.text.strip()
            
#         #     # Create a dictionary for this listing
#         #     listing_data = {
#         #         "title": title,
#         #         "price": price_value
#         #     }
            
            
     
            
#         #     # save listing_data to listing.json file
#         #     with open('listings.json', 'a', encoding='utf-8') as f:
#         #         json.dump(listing_data, f, ensure_ascii=False)
#         #         f.write('\n')
            
#     else:
#         print(f"Failed to retrieve the page. Status code: {response.status_code}")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     import traceback
#     print(traceback.format_exc())
    
    
# def load_existing_listings():
#     try:
#         if os.path.exists('listings.json'):
#             with open('listings.json', 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         return []
#     except json.JSONDecodeError:
#         logging.error("Error decoding JSON from listings.json. Starting with an empty list.")
#         return []
    
