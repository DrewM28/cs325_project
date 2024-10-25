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

I then had to strip the URL's to remove unneccesary white space
```urls = [url.strip() for url in urls]```


