from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import cloudscraper
from bs4 import BeautifulSoup
import time
import re  

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the ChromeDriver service using webdriver_manager
service = Service(ChromeDriverManager().install())

# Create a new Chrome driver instance
driver = webdriver.Chrome(service=service, options=chrome_options)
scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

url = "https://www.101evler.com/north-cyprus/houses-to-rent?page=1"

# Get the page content
response = scraper.get(url)
    
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
for link in soup.find_all('a'):
    print(link.get('href'))

listings = soup.find_all('div')


h4_elements = soup.find_all('h4', class_=re.compile(r'^text-block-'))
print(f"Found {len(h4_elements)} h4 elements with class starting with 'text-block-'")
price_elements = soup.find_all('div', class_='basicprice')
print(f"Found {len(price_elements)} div elements with class 'basicprice'")
for index, h4 in enumerate(h4_elements, 1):
    print(f"{index}. Class: {h4.get('class')}, Text: {h4.text.strip()}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
for index, price in enumerate(price_elements, 1):
    print(f"{index}. Price: {price.text.strip()}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


# print(f'listings: {listings}')
# print(f'listings: {len(listings)}')