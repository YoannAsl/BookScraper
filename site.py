import requests
import os
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/index.html"
url = "http://books.toscrape.com/index.html"

req = requests.get(url)
category_soup = soup(req.content, "html.parser")

categories = category_soup.find("ul", class_="nav").find("ul").find_all("li")


def main():
    for category in categories:
        filename = f"./csv/{category.a.text.strip().lower().replace(' ','_')}.csv"

        f = open(filename, "w", encoding="utf-8")
        headers = "product_code, product_page_url, title, description, image_url, number_available, price_excluding_tax, price_including_tax, review_rating \n"
        f.write(headers)

        url = urljoin(BASE_URL, category.a.get("href"))

        while True:
            r = requests.get(url)
            print("new category")
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

                image_url = urljoin(book_url, book_soup.img["src"])
                download_image(image_url, title, "images")
                f.write(
                    f'{product_code},{book_url},{title.replace(",", "|")},{description.replace(",", "|")},{image_url},{number_available},{price_excluding_tax},{price_including_tax},{review_rating} \n'
                )
            # Selects the Next button, if there is none, closes the csv file and ends the loop
            next_page_button = category_soup.select_one("li.next > a")
            if next_page_button:
                next_page_url = next_page_button.get("href")
                url = urljoin(url, next_page_url)
            else:
                f.close()
                break


def download_image(url: str, name: str, path: str):
    if not os.path.isdir(path):
        os.makedirs(path)
    response = requests.get(url)
    image_name = f"{path}/{name.replace(' ','_').replace(':','')}.jpg"

    b = open(image_name, "wb")
    b.write(response.content)

    print(image_name)
    print(url)


main()
