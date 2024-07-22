import cloudscraper
from bs4 import BeautifulSoup
import re
import json
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create a scraper instance
scraper = cloudscraper.create_scraper(delay=10, browser='chrome')


def load_existing_listings():
    try:
        if os.path.exists('listings.json'):
            with open('listings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except json.JSONDecodeError:
        logging.error(
            "Error decoding JSON from listings.json. Starting with an empty list.")
        return []


def scrape_listings(url):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')

    try:
        response = scraper.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        h4_elements = soup.find_all('h4', class_=re.compile(r'^text-block-'))
        price_elements = soup.find_all('div', class_='basicprice')
        location_elements = soup.find_all('div', class_='locationpremiumdiv')

        new_listings = []
        for h4, price, location in zip(h4_elements, price_elements, location_elements):
            title = h4.text.strip()
            price_value = price.text.strip()
            location_value = location.text.strip()

            # Split location_value into parts
            location_parts = location_value.split('\n')

            # Extract location (combining the first two non-empty parts)
            location = ' '.join([part.strip()
                                for part in location_parts[:3] if part.strip()])

            # Extract area and rooms
            area = ''
            rooms = ''
            for part in location_parts[3:]:
                part = part.strip()
                if 'm²' in part:
                    area = part
                elif '+' in part:
                    rooms = part

            listing_data = {
                "title": title,
                "price": price_value,
                "location": location,
                "area": area,
                "rooms": rooms,
                "scraped_at": datetime.now().isoformat()
            }

            new_listings.append(listing_data)
            logging.info(
                f"Scraped: {title} - {price_value} - {location} - {area} - {rooms}")

        return new_listings

    except Exception as e:
        logging.error(f"Error scraping {url}: {str(e)}")
        return []


def save_listings(new_listings):
    existing_listings = load_existing_listings()

    # Combine existing listings with new listings
    updated_listings = existing_listings + new_listings

    # Remove duplicates
    unique_listings = []
    seen = set()
    for listing in updated_listings:
        # Create a tuple of the listing's key attributes
        listing_key = (listing['title'], listing['price'],
                       listing['location'], listing['area'], listing['rooms'])
        if listing_key not in seen:
            seen.add(listing_key)
            unique_listings.append(listing)

    # Write the combined list back to the file
    with open('listings.json', 'w', encoding='utf-8') as f:
        json.dump(unique_listings, f, ensure_ascii=False, indent=2)

    logging.info(
        f"Added {len(new_listings)} new listings. Total unique listings: {len(unique_listings)}")


def main():
    url = "https://www.101evler.com/north-cyprus/houses-to-rent?page=1"

    new_listings = scrape_listings(url)

    if new_listings:
        save_listings(new_listings)
    else:
        logging.info("No new listings found.")


if __name__ == "__main__":
    main()

# load_existing_listings()
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
