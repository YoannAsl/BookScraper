import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin

url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"


def main():
    # Creates and opens the .csv file
    filename = "category.csv"
    f = open(filename, "w")

    # Headers of the .csv file
    headers = "product_code, product_page_url, title, description, category, image_url, number_available, price_excluding_tax, price_including_tax, review_rating \n"

    f.write(headers)

    while True:
        r = requests.get(url)

        # HTML parsing
        category_soup = soup(r.content, "html.parser")

        # Gets all books from the page
        books = category_soup.find_all("li", class_="col-xs-6")

        for book in books:
            book_url = urljoin(url, book.a["href"])

            book_html = requests.get(book_url)
            book_soup = soup(book_html.content, "html.parser")

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

            image_url = urljoin(book_url, book_soup.img["src"])
            f.write(
                f'{product_code},{book_url},{title.replace(",", "|")},{description.replace(",", "|")},{category},{image_url},{number_available},{price_excluding_tax},{price_including_tax},{review_rating} \n'
            )
        # Selects the Next button, if there is none, closes the csv file and ends the loop
        next_page_button = category_soup.select_one("li.next > a")
        if next_page_button:
            next_page_url = next_page_button.get("href")
            url = urljoin(url, next_page_url)
        else:
            f.close()
            break
