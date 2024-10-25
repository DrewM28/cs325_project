#Drew Milton

import requests
from bs4 import BeautifulSoup
import time

#Pauses the execution every 2 seconds as to not overload the website
time.sleep(2)

#Opens my URL.txt file and reads the url's inside it
with open('URL.txt', 'r') as url_file:
    urls = url_file.readlines()

#Remove any extra spaces or newlines from the URLs
urls = [url.strip() for url in urls]

#Header that makes it look like a browser
headers = {
    'User-Agent': 'Mozilla/5.0 '
}


#For loop to go through each url and gives them a starting index of 1 to enumerate from
for i, url in enumerate(urls, start=1):
    print(f"Scraping URL {i}: {url}")

    #Opens up the URL
    response = requests.get(url, headers=headers, timeout=30)

    #Checks to make sure the URL opened correctly
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser') #Using beautiful soup to scrape the website

        #Sets an empty reviews array then finds all the reviews using beautiful soup
        reviews = []
        review_elements = soup.find_all('p', class_='pre-white-space')

        #If statement to check if there is a review then append it to reviews array
        if review_elements:
            for review in review_elements:
                review_text = review.get_text(strip=True)
                reviews.append(f"{review_text}\n\n")

            #Created a review_{index}.txt file to write the reviews to
            with open(f'review_{index}.txt', 'w', encoding='utf-8') as file:
                file.writelines(reviews)

            #Optional Print statements to make sure the scraping is complete
            print(f"Scraping complete. Comments saved to review_{i}.txt")
        else:
            print(f"No reviews found for URL {i}: {url}")
    else:
        print(f"Failed to retrieve URL {i}. Status code: {response.status_code}")

