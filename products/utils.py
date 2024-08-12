import requests
from bs4 import BeautifulSoup
import time
import re

# Function to make a web request with retries
def make_request(url, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url)
            # Return the response if the request was successful
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            # Print an error message if the request fails
            print('Error making request:', e)
        # Wait for 1 second before retrying to avoid overwhelming the server
        time.sleep(1)
    # Return None if all retries fail
    return None

# Function to scrape data from a Flipkart product page
def flipkart_scrapper(url):
    response = make_request(url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the product title
        title = soup.find('span', class_='B_NuCI')
        if title is not None:
            title = title.get_text(strip=True)
        # Extract the product price and convert it to an integer
        price_element = soup.find('div', class_='_30jeq3 _16Jk6d')
        if price_element:
            price = int(re.sub(r'\D', '', price_element.get_text(strip=True)))
        else:
            price = None
        # Extract the image URL
        image_element = soup.select_one('img._2r_T1I._396QI4, img._396cs4._2amPTt._3qGmMb')
        image = image_element['src'] if image_element else None
        # Return the scraped data
        return {'title': title, 'price': price, 'img_link': image}
    else:
        # Return an error message if the request fails
        return {'error': 'Failed to fetch data from URL'}

# Function to scrape data from an eBay product page
def ebay_scrapper(url):
    response = make_request(url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the product title
        title_element = soup.find('span', class_='ux-textspans ux-textspans--BOLD')
        title = title_element.get_text(strip=True) if title_element else None
        # Extract the product price, convert it to a float, then to an integer representing cents
        price_element = soup.find('div', class_='x-price-primary').find('span', class_='ux-textspans')
        price = None
        if price_element:
            price_text = re.sub(r'[^\d.]', '', price_element.get_text(strip=True))
            try:
                price = int(float(price_text) * 100)
            except ValueError:
                print("Price conversion error")
                price = None
        # Extract the image URL
        image_element = soup.find('div', class_='ux-image-carousel-item')
        img_link = None
        if image_element and image_element.find('img'):
            img_link = image_element.find('img')['src']
        # Return the scraped data
        return {'title': title, 'price': price, 'img_link': img_link}
    else:
        # Return an error message if the request fails
        return {'error': 'Failed to fetch data from URL'}
