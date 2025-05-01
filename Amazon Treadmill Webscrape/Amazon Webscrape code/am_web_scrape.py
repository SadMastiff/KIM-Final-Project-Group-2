from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

search_query = 'treadmills'.replace(' ', '+') 
base_url = f'https://www.amazon.com/s?k={search_query}'

items = []
seen_products = set()

for i in range(1, 21):  #Scrapping 20 pages 
    print(f'Processing {base_url}&page={i}...')
    response = requests.get(f'{base_url}&page={i}', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        title_tag = result.h2
        if not title_tag:
            continue

        product_name = title_tag.text.strip()

        #Getting ratings
        rating_tag = result.find('span', {'class': 'a-icon-alt'})
        rating = rating_tag.text.strip() if rating_tag else 'N/A'

        #Getting rating count
        rating_count_tag = result.find('span', {'class': 'a-size-base s-underline-text'})
        rating_count = rating_count_tag.text.strip() if rating_count_tag else 'N/A'

        #Getting price
        price_tag = result.find('span', {'class': 'a-offscreen'})
        price = price_tag.text.strip().replace('$', '') if price_tag else 'N/A'

        #Creating a unique identifier using multiple fields
        product_key = (product_name, rating, price)

        if product_key in seen_products:
            continue  #Checking for duplicates 
        seen_products.add(product_key)

        items.append([product_name, rating, rating_count, price])

    sleep(2)

#Save to CSV
df = pd.DataFrame(items, columns=['Product Name', 'Rating', 'Rating Count', 'Price'])
df.to_csv('amazon_treadmills_clean.csv', index=False)
print("Scraping complete. Data saved to 'amazon_treadmills_clean.csv'")
