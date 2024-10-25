Project 2 WebScraper

To start this project I imported requests to send a request to the URL, I imported BeautifulSoup to scrape the HTML off the URL, and I imported time to pause the execution
```import requests```
```from bs4 import BeautifulSoup```
```import time```

After imported this is where I used my time.sleep to pause the execution so the it doesn't block the website with 4 immediate requests
```time.sleep(2)```

I then opened my URL.txt file to read in the URL's
```with open('URL.txt', 'r') as url_file:```
    ```urls = url_file.readlines()```

I then had to strip the URL's to remove unneccesary white space and I used a for to go through each URL
```urls = [url.strip() for url in urls]```

I then had to use a header to mimic a browser
```headers = { ```
    ```'User-Agent': 'Mozilla/5.0'```
    ```}```

Next I used a for loop to go through each URL starting at 1 so in the end it will write the file with a 1 instead of 0
```for i, url in enumerate(urls, start=1):```

I put in an optional print statement after this to make sure it gets to this point and lets me know it is working correctly through the for loop
```print(f"Scraping URL {i}: {url}")```

This is the part where I use requests to request to open the URL using the URL and header with a timeout of 30 so the website won't time me out after 30 seconds
```response = requests.get(url, headers=headers, timeout=30)```

Now I use an if statement to make sure that after I open the URL there is no problems with the website
```if response.status_code == 200:```
This says that if the status code of the website = 200 then it is working fine and opened the website

Now I use BeautifulSoup which is why I needed to import it in the beginning
```soup = BeautifulSoup(response.content, 'html-parser')```

I then make an empty array and set that to reviews and make a review_elements that finds all the <p> with class pre-white-space that contains reviews
```reviews = []```
```review_elements = soup.find_all('p', class_ =  'pre-white-space')```

Now there is an If statement afterwards to check that review_elements returned something
```if review_elements:```

After this there is a for loop to get the text from review_elemets and store it in review_text then append that to the empty array reviews
```for review in review_elements:```
    ```review_text = review.get_text(strip == true)```
    ```reviews.append(f"{review_text}\n\n)```

Now to final parts where I create the review.txt files and write to them using the array reviews
```with open(f'review_{i}.txt, 'w' encoding = 'utf-8) as file:```
    ```file.writelines(reviews)```

The very last lines are optional because they are print statements but I think it was nice to include for testing purposes to see what happens
The first print is inside the big if statement
```print(f"Scraping complete. Comments saved to review_{i}.txt")```
After we have the else statement in case the if fails
```else:```
    ```print(f"No reviews found for URL {i}: {url}")```
Finally the last print statement is for the if from the beginning if it can't get the URL
```else:```
    ```print(f"Failed to retrieve URL {i}. Status code: {response.status_code}")```


