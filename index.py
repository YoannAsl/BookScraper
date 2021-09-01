from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

uClient = uReq(url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# Creates and opens the .csv file
filename = "books.csv"
f = open(filename, "w")

# NEED TO ADD PRODUCT URL
# Headers of the .csv file
headers = "product_code, title, description, category, image_url, number_available, price_excluding_tax, price_including_tax, review_rating \n"

f.write(headers)

# Table that contains a bunch of information we need
table = page_soup.findAll("tr")

product_code = table[0].td.text
price_excluding_tax = table[2].td.text
price_including_tax = table[3].td.text
number_available = table[5].td.text

title = page_soup.h1.text
description = page_soup.findAll("p")[3].text
review_rating = page_soup.findAll("p", {"class": "star-rating"})[0]["class"][1]
category = page_soup.findAll("a")[3].text

scraped_url = page_soup.img["src"]
image_url = "http://books.toscrape.com/" + scraped_url[6:]

f.write(
    product_code
    + ","
    + title.replace(",", "|")
    + ","
    + description.replace(",", "|")
    + ","
    + category
    + ","
    + image_url
    + ","
    + number_available
    + ","
    + price_excluding_tax
    + ","
    + price_including_tax
    + ","
    + review_rating
    + "\n"
)

f.close()
