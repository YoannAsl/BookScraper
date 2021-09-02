import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin

base_url = "http://books.toscrape.com/index.html"
url = "http://books.toscrape.com/index.html"

req = requests.get(url)
category_soup = soup(req.content, "html.parser")

categories = category_soup.find("ul", class_="nav").find("ul").find_all("li")
for category in categories:
    filename = f"{category.a.text.strip().lower().replace(' ','_')}.csv"

    f = open(filename, "w", encoding="utf-8")
    headers = "product_code, product_page_url, title, description, image_url, number_available, price_excluding_tax, price_including_tax, review_rating \n"
    f.write(headers)

    url = urljoin(base_url, category.a.get("href"))
    print(url)
    while True:
        r = requests.get(url)
        print("new category")
        # HTML parsing
        category_soup = soup(r.content, "html.parser")

        # Gets all books from the page
        books = category_soup.find_all("li", class_="col-xs-6")
        print(len(books))
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
            print(title)

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
