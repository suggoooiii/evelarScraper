import cloudscraper
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the ChromeDriver service using webdriver_manager
service = Service(ChromeDriverManager().install())

# Create a new Chrome driver instance
driver = webdriver.Chrome(service=service, options=chrome_options)
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
        
        # Find all div elements with class="basicilandiv"
        listings = soup.find_all('div', class_='basicprice')
        
        print(f"Found {len(listings)} listings")
        
        # List to store all listing data
        all_listings = []
        
        # Extract information from each listing
        for index, listing in enumerate(listings, 1):
            # Find the title (h4 with class starting with "text-block-")
            title_element = listing.find('h4', class_=re.compile(r'^text-block-'))
            print(f'title_element: {title_element}')
            title = title_element.text.strip() if title_element else "N/A"
            
            # Find the price (div with class "basicprice")
            price_element = listing.find('div', class_='basicprice')
            print(f'price_element: {price_element}')
            price = price_element.text.strip() if price_element else "N/A"
            
            # Create a dictionary for this listing
            listing_data = {
                "title": title,
                "price": price
            }
            
            all_listings.append(listing_data)
            
            print(f"Listing {index}:")
            print(f"  Title: {title}")
            print(f"  Price: {price}")
            print("---")
        
        # Save the data to a JSON file
        with open('listings.json', 'w', encoding='utf-8') as f:
            json.dump(all_listings, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to listings.json")
        
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    print(traceback.format_exc())