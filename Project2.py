#Drew Milton

import requests
#using beautiful soup to give a nested data structure
from bs4 import BeautifulSoup


url = "https://www.bestbuy.com/site/reviews/apple-watch-se-2nd-generation-gps-44mm-midnight-aluminum-case-with-midnight-sport-band-m-l-midnight/6340310?variant=A"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)
#print("Before if statement")

if response.status_code == 200:
    print("Request successful")
    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = []
    review_elements = soup.find_all('div', class_='review')
    print("Before for loop")

    for review in review_elements:
        reviewer_name = review.find('span', class_='review-name').get_text(strip=True)
        review_text = review.find('div', class_='review-text').get_text(strip=True)
        rating = review.find('span', class_='review-rating').get_text(strip=True)
        review_date = review.find('span', class_='review-date').get_text(strip=True)

        formatted_review = f"Reviewer: {reviewer_name}\nRating: {rating}\nDate: {review_date}\nReview: {review_text}\n\n"

        reviews.append(formatted_review)  

    with open('reviews.txt', 'w', encoding='utf-8') as file:
            file.writelines(reviews)

    print('Scraping complete. Reviews saved to reviews.csv')

else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')

