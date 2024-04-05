import re
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

import requests
from bs4 import BeautifulSoup


class ProducthuntData:
    def __init__(self, app_slug):
        self.app_slug = app_slug
        self.base_url = "https://www.producthunt.com"
        self.rates_url = f"{self.base_url}/products/{self.app_slug}/reviews"
        self.app_url = f"{self.base_url}/products/{self.app_slug}"
        self.app_info = {}

    # taking rates (n/5)
    def get_rates(self):
        response = requests.get(self.rates_url)
        print(self.rates_url, '-rates_url')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the desired div element
        rating_element = soup.select_one('.text-32.font-semibold.text-dark-grey.styles_reviewPositive__JY_9N.mb-2')

        if rating_element:
            # Extract the text content of the div element
            rating_text = rating_element.get_text(strip=True)

            # Use regular expression to extract the rating and number of reviews
            rating_match = re.search(r'(\d+(\.\d+)?)\/5.*\(([\d,]+) reviews\)', rating_text)
            if rating_match:
                rating = rating_match.group(1)
                self.app_info['rating'] = rating
                return self.app_info['rating']

    # taking reviews quantity
    def get_reviews_quantity(self):
        response = requests.get(self.rates_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the desired div element
        rating_element = soup.select_one('.text-32.font-semibold.text-dark-grey.styles_reviewPositive__JY_9N.mb-2')

        if rating_element:
            # Extract the text content of the div element
            rating_text = rating_element.get_text(strip=True)

            # Use regular expression to extract the rating and number of reviews
            rating_match = re.search(r'(\d+(\.\d+)?)\/5.*\(([\d,]+) reviews\)', rating_text)
            if rating_match:
                num_reviews = rating_match.group(3).replace(',', '')  # Remove commas from the number
                self.app_info['num_reviews'] = num_reviews
                return self.app_info['num_reviews']

    # taking description
    def get_desc(self):
        response = requests.get(self.app_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        description_element = soup.select_one('.text-16.font-normal.text-light-grey.mb-6')

        if description_element:
            description = description_element.get_text(strip=True)
            self.app_info['description'] = description
            return self.app_info['description']

    # taking link
    def get_link(self):
        response = requests.get(self.app_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Найти элемент, содержащий ссылку на сайт
        website_element = soup.find('a', {'data-test': 'product-header-visit-button'})

        if website_element:
            # Получить значение атрибута 'href', содержащее URL-адрес
            website_url = website_element.get('href')

            # Обрезать параметр 'ref' из URL-адреса, если он существует
            parsed_url = urlparse(website_url)
            query_params = parse_qs(parsed_url.query)
            if 'ref' in query_params:
                del query_params['ref']
            website_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params,
                                      urlencode(query_params), parsed_url.fragment))

            self.app_info['website_url'] = website_url
            return self.app_info['website_url']