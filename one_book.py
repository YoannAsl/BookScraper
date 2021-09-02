import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin

url = "http://books.toscrape.com/catalogue/blood-defense-samantha-brinkman-1_8/index.html"

r = requests.get(url)

# HTML parsing
page_soup = soup(r.content, "html.parser")

# Creates and opens the .csv file
filename = "one_book.csv"
f = open(filename, "w")

# Headers of the .csv file
headers = "product_code, product_page_url, title, description, category, image_url, number_available, price_excluding_tax, price_including_tax, review_rating \n"

f.write(headers)

# Table that contains a bunch of information we need
table = page_soup.find_all("tr")

product_code = table[0].td.text
price_excluding_tax = table[2].td.text
price_including_tax = table[3].td.text
number_available = table[5].td.text

title = page_soup.h1.text
description = page_soup.find_all("p")[3].text
review_rating = page_soup.find("p", {"class": "star-rating"})["class"][1]
category = page_soup.find_all("a")[3].text

image_url = urljoin(url, page_soup.img["src"])

f.write(
    f'{product_code},{url},{title.replace(",", "|")},{description.replace(",", "|")},{category},{image_url},{number_available},{price_excluding_tax},{price_including_tax},{review_rating} \n'
)

f.close()
