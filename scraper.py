import requests
from bs4 import BeautifulSoup
import json

url = "https://www.101evler.com/north-cyprus/houses-to-rent?page=1"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

listings = soup.find_all('div', class_='listing')  # Adjust class as per actual HTML

data = []
for listing in listings:
    photos = [img['src'] for img in listing.find_all('img')]  # Example, adjust as needed
    location = listing.find('div', class_='location').text.strip()  # Adjust class as needed
    price = listing.find('div', class_='price').text.strip()  # Adjust class as needed
    min_rental_period = listing.find('div', class_='rental-period').text.strip()  # Adjust class as needed
    payment_interval = listing.find('div', class_='payment-interval').text.strip()  # Adjust class as needed
    last_updated = listing.find('div', class_='last-updated').text.strip()  # Adjust class as needed

    data.append({
        'photos': photos,
        'location': location,
        'price': price,
        'min_rental_period': min_rental_period,
        'payment_interval': payment_interval,
        'last_updated': last_updated,
    })

# Save data to a JSON file
with open('listings.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data scraped successfully!")