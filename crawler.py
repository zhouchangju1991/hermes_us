import requests, json
from datetime import datetime
import pytz

class Crawler:
    def __init__(self):
        self.__request_session = requests.Session()
        self.__request_headers = {
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        }

    def fetch_skus_by_keyword(self, keyword):
        skus = []
        initial_response = self.__get('https://bck.hermes.com/product?locale=us_en&searchterm={}'.format(keyword))
        products_num = json.loads(initial_response.text)['total']
        offset = 0
        while offset < products_num:
            products_response = self.__get('https://bck.hermes.com/product?locale=us_en&searchterm={}&offset={}'.format(keyword, offset))
            products_json = json.loads(products_response.text)
            products = products_json['products']['items']
            for product in products:
                skus.append(product['sku'])
            offset += 36

        return skus

    def fetch_product_by_sku(self, sku, keyword):
        response = self.__get('https://bck.hermes.com/product-page?locale=us_en&productsku={}'.format(sku))
        product_json = json.loads(response.text)
        product = {
            'sku': sku,
            'pattern': formalize(product_json['title']),
            'images': ['https:{}'.format(image['url']) for image in product_json['assets']],
            'price': product_json['price'],
            'url': 'https://www.hermes.com{}'.format(product_json['url']),
            'slug': formalize(product_json['slug']),
            'published': product_json['hasStock'],
            'description_html': product_json['simpleAttributes']['description'],
            'dimension': product_json['simpleAttributes']['dimensions'],
            'color': product_json['simpleAttributes']['colorHermes'],
            'updated_at': datetime.now(pytz.timezone('US/Pacific')),
            'keyword': keyword,
        }

        return product

    def __get(self, url):
        return self.__request_session.get(url, headers=self.__request_headers)

def formalize(s):
    if None == s or '' == s:
        return ''
    return s.lower().strip()
