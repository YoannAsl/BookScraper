from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

category_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
base_book_url = "http://books.toscrape.com/catalogue"

uClient = uReq(category_url)
category_html = uClient.read()
uClient.close()

# Creates and opens the .csv file
filename = "category.csv"
f = open(filename, "w")

# Headers of the .csv file
headers = "product_code, product_page_url, title, description, category, image_url, number_available, price_excluding_tax, price_including_tax, review_rating \n"

f.write(headers)

# HTML parsing
category_soup = soup(category_html, "html.parser")

books = category_soup.find_all("li", class_="col-xs-6")

for book in books:
    book_url = base_book_url + book.a["href"][8:]

    bookClient = uReq(book_url)
    book_html = bookClient.read()
    bookClient.close()
    book_soup = soup(book_html, "html.parser")

    # Table that contains a bunch of information we need
    table = book_soup.find_all("tr")

    product_code = table[0].td.text
    price_excluding_tax = table[2].td.text
    price_including_tax = table[3].td.text
    number_available = table[5].td.text

    title = book_soup.h1.text
    description = book_soup.find_all("p")[3].text
    review_rating = book_soup.find("p", class_="star-rating")["class"][1]
    category = book_soup.find_all("a")[3].text

    scraped_url = book_soup.img["src"]
    image_url = "http://books.toscrape.com/" + scraped_url[6:]

    f.write(
        f'{product_code},{book_url},{title.replace(",", "|")},{description.replace(",", "|")},{category},{image_url},{number_available},{price_excluding_tax},{price_including_tax},{review_rating} \n'
    )
f.close()
