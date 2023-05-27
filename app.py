import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listings(url, pages):
    product_data = []
    
    for page in range(1, pages + 1):
        page_url = url + f'&page={page}'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for product in products:
            product_url = product.find('a', {'class': 'a-link-normal'})['href']
            product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
            product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
            rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()
            
            product_data.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of Reviews': num_reviews
            })
    
    return product_data

def scrape_product_details(product_urls):
    product_details = []
    
    for url in product_urls:
        # Check if the URL has a scheme (e.g., "http://" or "https://")
        if not url.startswith('http'):
            url = 'https://www.amazon.in' + url
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        asin = soup.find('input', {'id': 'ASIN'})['value']
        description = soup.find('div', {'id': 'productTitle'}).text.strip()
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
        product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
        
        product_details.append({
            'Product URL': url,
            'ASIN': asin,
            'Description': description,
            'Manufacturer': manufacturer,
            'Product Description': product_description
        })
    
    return product_details


# Part 1: Scraping Product Listings

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
num_pages = 20

product_listings = scrape_product_listings(base_url, num_pages)

csv_file = 'product_listings.csv'
fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_listings)

# Part 2: Scraping Product Details

product_urls = [listing['Product URL'] for listing in product_listings]

product_details = scrape_product_details(product_urls[:200])

csv_file = 'product_details.csv'
fieldnames = ['Product URL', 'ASIN', 'Description', 'Manufacturer', 'Product Description']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_details)
