import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'

# Initialize page number
page_number = 1
books = []

while True:
    # Format the URL with the current page number
    url = base_url.format(page_number)
    
    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all book titles and prices
        book_items = soup.find_all('article', class_='product_pod')

        # If no books are found, break the loop
        if not book_items:
            break
        
        for book in book_items:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            books.append({'title': title, 'price': price})

        print(f'Scraped page {page_number}.')

        # Increment the page number for the next iteration
        page_number += 1
    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
        break

# Save the scraped data to a JSON file
with open('books.json', 'w') as json_file:
    json.dump(books, json_file, indent=4)

print("Data saved to books.json")
