
#The following scrapping is done for amazon - Best laptop for students

import time
import random
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

product_name = []
price = []
review = []

for i in range(2, 30):
    url = f'https://www.amazon.com/s?k=best+laptops+for+college+students&page={i}&crid=ELQIVLDHECC8&qid=1724930039&sprefix=best+laptops+%2Caps%2C399&ref=sr_pg_2'
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }

    page = requests.get(url, headers=headers)
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        product_titles = soup.find_all('span', class_='a-size-medium a-color-base a-text-normal')
        for title in product_titles:
            name = title.text.strip()
            product_name.append(name)

        price_titles = soup.find_all('span', class_="a-offscreen")
        for price_tag in price_titles:
            price.append(price_tag.text.strip())

        review_titles = soup.find_all('span', class_="a-icon-alt")
        for review_tag in review_titles:
            review_text = review_tag.text.strip()
            if re.match(r'^\d+(\.\d+)? out of \d+ stars$', review_text):
                final_review = review_text.split(' ')[0]
                review.append(final_review)

        print(f"Page {i} scraped successfully.")

    else:
        print(f"Failed to retrieve page {i}. Status code: {page.status_code}")

    # Random delay between requests to avoid triggering anti-scraping mechanisms
    time.sleep(random.uniform(3, 6))

# Ensure all lists are the same length
min_length = min(len(product_name), len(price), len(review))
product_name = product_name[:min_length]
price = price[:min_length]
review = review[:min_length]

# Create DataFrame
data = {
    'Product Name': product_name,
    'Price': price,
    'Review': review
}

df = pd.DataFrame(data)

# Display sample data
print("\nSample Data:")
print(df.head())

# Optionally, save to a CSV file
df.to_csv('amazon_laptops.csv', index=False)
