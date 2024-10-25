import requests
from bs4 import BeautifulSoup
import time

#pauses the execution every 2 seconds as to not overload the website
time.sleep(2)

# Open and read the URLs from the URL.txt file
with open('URL.txt', 'r') as url_file:
    urls = url_file.readlines()

# Remove any extra spaces or newlines from the URLs
urls = [url.strip() for url in urls]

# Custom headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 '
}


# Loop through each URL in the URL.txt file
for i, url in enumerate(urls, start=1):
    print(f"Scraping URL {i}: {url}")

    # Send a request to the URL
    response = requests.get(url, headers=headers, timeout=30)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract only the review text (you may need to adjust class names based on the website's structure)
        reviews = []
        review_elements = soup.find_all('p', class_='pre-white-space')  # Adjust class if necessary

        # Check if there are reviews to scrape
        if review_elements:
            for review in review_elements:
                review_text = review.get_text(strip=True)  # Extract only the review comment text
                reviews.append(f"{review_text}\n\n")  # Add the review text to the list

            # Save the comments to a file, naming it 'review_1.txt', 'review_2.txt', etc.
            with open(f'review_{index}.txt', 'w', encoding='utf-8') as file:
                file.writelines(reviews)

            print(f"Scraping complete. Comments saved to review_{i}.txt")
        else:
            print(f"No reviews found for URL {i}: {url}")
    else:
        print(f"Failed to retrieve URL {i}. Status code: {response.status_code}")

