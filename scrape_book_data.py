# Importing libraries
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import random

# Initialize lists to store extracted data
Book_title = []
Book_price = []
Book_review = []
Total_no_review = []
Author = []

# Connecting to the site and extracting data
for i in range(1, 30):
    url = f'https://www.amazon.com/s?k=best+books+to+buy&page={i}&crid=HB8CEHSZKU1I&qid=1725092926&sprefix=best+books+to+buy%2Caps%2C397&ref=sr_pg_{i}'
    header = {
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

    response = requests.get(url, headers=header)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            print('Connection Established:', response.status_code)
        else:
            print(f'Failed to retrieve data..{response.status_code}')
            continue  # Skip to the next iteration if the response is not successful
    except Exception as e:
        print(response.status_code, ': Connection Lost', e)
        continue  # Skip to the next iteration if there's an error

    # Extract product titles
    product_titles = soup.find_all('span', class_='a-size-medium a-color-base a-text-normal')
    for title_element in product_titles:
        title = title_element.text.strip() if title_element else 'NULL'
        Book_title.append(title)  # Append to list

    # Extract prices, handling missing values
    price_elements = soup.find_all('span', class_="a-offscreen")
    for price_element in price_elements:
        price = price_element.text.strip() if price_element else 'NULL'
        Book_price.append(price)  # Append to list

    # Extract reviews, handling missing values
    review_elements = soup.find_all('span', class_="a-icon-alt")
    for review_element in review_elements:
        review_text = review_element.text.strip() if review_element else 'NULL'
        if re.match(r'^\d+(\.\d+)? out of \d+ stars$', review_text):
            final_review = review_text.split(' ')[0]
            Book_review.append(final_review)  # Append to list
        else:
            Book_review.append('NULL')  # Append 'NULL' if pattern doesn't match

    # Extract number of reviews, handling missing values
    no_of_review_elements = soup.find_all('span', class_="a-size-base s-underline-text")
    for no_of_review_element in no_of_review_elements:
        no_of_review = no_of_review_element.text.strip() if no_of_review_element else 'NULL'
        Total_no_review.append(no_of_review)  # Append to list

    # Extract author names, handling missing values
    author_name_elements = soup.find_all('a', class_="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style")
    for author_name_element in author_name_elements:
        author_name = author_name_element.get_text().strip() if author_name_element else 'NULL'
        Author.append(author_name)  # Append to list

    print(f'Page {i} Data Extracted... 200')

    # Random delay between requests to avoid being blocked
    time.sleep(random.uniform(3, 6))

# Ensure all lists have the same length by filling missing entries with 'NULL'
max_length = max(len(Book_title), len(Book_price), len(Book_review), len(Total_no_review), len(Author))

# Extend lists to match max_length
Book_title.extend(['NULL'] * (max_length - len(Book_title)))
Book_price.extend(['NULL'] * (max_length - len(Book_price)))
Book_review.extend(['NULL'] * (max_length - len(Book_review)))
Total_no_review.extend(['NULL'] * (max_length - len(Total_no_review)))
Author.extend(['NULL'] * (max_length - len(Author)))

# Create a DataFrame
data = {
    'Title': Book_title,
    'Author': Author,
    'Review': Book_review,
    'Total Reviews': Total_no_review,
    'Price': Book_price,
}

df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Function to save DataFrame to a CSV file
def save_to_csv(df, filename='books_data.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Save the DataFrame to a CSV file
save_to_csv(df)
