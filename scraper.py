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

listings = soup.find('div', class_='basicilandiv')