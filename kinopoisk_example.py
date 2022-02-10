import re
import time

import requests
from bs4 import BeautifulSoup

ENDPOINT_URL = "https://www.kinopoisk.ru/lists/movies/series-top250/"
PARAMS = {"page": 1}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}
# regexp in bs4!
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#a-regular-expression
BS_CLASSES = {
    "elements": re.compile("styles_content__.*"),
    "name": re.compile("styles_mainTitle__.*"),
    "original_name": re.compile("desktop-list-main-info_secondaryText__.*"),
    "rating": re.compile(".*styles_kinopoiskValue__.*"),
}


class KinopoiskScraper:
    def __init__(self, start_url, params, headers):
        self.headers = headers
        self.start_url = start_url
        self.start_params = params
        self.info_about_films = []

    def get_html_string(self, url, params):
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            time.sleep(1)
            print(e)
            return None
        return response.text

    @staticmethod
    def get_dom(html_string):
        return BeautifulSoup(html_string, "html.parser")

    def run(self):
        self.paginate(self.start_url, self.start_params)
        # or get it from the page?
        for page_number in range(2, 5):
            params = self.start_params
            params["page"] = page_number
            self.paginate(self.start_url, params)

    def extract_text(self, element, cls):
        return element.find(attrs={"class": BS_CLASSES[cls]}).text

    def get_info_from_element(self, element):
        info = {}
        info["name"] = self.extract_text(element, "name")
        info["original_name"] = self.extract_text(element, "original_name")
        try:
            rating_element = self.extract_text(element, "rating")
            info["rating"] = rating_element.text
            info["rating"] = float(info["rating"])
        except AttributeError as e:
            print(e)
        except ValueError as e:
            print(e)
        return info

    def save_info_about_films(self):
        # TODO
        # with open(...) as f:
        pass

    # only to page 2
    def paginate(self, url, params):
        html_string = self.get_html_string(url, params)
        if html_string is None:
            print("There was an error")
            return

        soup = KinopoiskScraper.get_dom(html_string)
        film_elements = list(
            map(
                lambda x: x.parent,
                soup.find_all("div", attrs={"class": BS_CLASSES["elements"]}),
            )
        )
        for element in film_elements:
            info = self.get_info_from_element(element)
            self.info_about_films.append(info)


if __name__ == "__main__":
    scraper = KinopoiskScraper(ENDPOINT_URL, PARAMS, HEADERS)
    scraper.run()
    print()
    scraper.save_info_about_films()
