import cloudscraper
from bs4 import BeautifulSoup
import re
import json

# Create a scraper instance
scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

url = "https://www.101evler.com/north-cyprus/houses-to-rent?page=1"

try:
    # Get the page content
    response = scraper.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all h4 elements with class starting with "text-block-"
        h4_elements = soup.find_all('h4', class_=re.compile(r'^text-block-'))
        
        # Find all div elements with class "basicprice"
        price_elements = soup.find_all('div', class_='basicprice')
        
        # List to store all listing data
        all_listings = []
        
        # Extract information from each listing
        for h4, price in zip(h4_elements, price_elements):
            # print(f'h4: {h4} price: {price}')
            title = h4.text.strip()
            price_value = price.text.strip()
            
            # Create a dictionary for this listing
            listing_data = {
                "title": title,
                "price": price_value
            }
            
            
            print(f"Listing:")
            print(f"  Title: {title}")
            print(f"  Price: {price_value}")
            print("---")

        # Save tlisting_data to a JSON file
        
         
                
        
        # with open('listings.json', 'w', encoding='utf-8') as f:
        #     json.dump(all_listings, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to listings.json")
        
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    print(traceback.format_exc())