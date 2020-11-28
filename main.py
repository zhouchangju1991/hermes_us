from datetime import datetime
import pytz
from crawler import Crawler
from database import Database
from mailer import Mailer
from log import Log

# Creates a log object. The log file name is today's date.
log = Log()

# Create database object
try:
    database = Database()
except Exception as exception:
    log.error('Fail to create Database object. Error message: {}'.format(exception))
    exit()

# Create crawler object
try:
    crawler = Crawler()
except Exception as exception:
    log.error('Fail to create Crawler object. Error message: {}'.format(exception))
    exit()

# Create email object
try:
    mailer = Mailer()
except Exception as exception:
    log.error('Fail to create Mailer object. Error message: {}'.format(exception))
    exit()

def main():
    keyword_docs = database.collection('hermes_us_keyword').where('is_valid', '==', True).stream()
    keywords = [doc.to_dict()['keyword'] for doc in keyword_docs]
    skus = []
    for keyword in keywords:
        for sku in crawler.fetch_skus_by_keyword(keyword):
            if sku in skus:
                continue
            product = crawler.fetch_product_by_sku(sku, keyword)
            if not product or not product['published']:
                log.info('{} is fetched while the product is out of stock'.format(sku))
                continue
            check_product(product)
            skus.append(sku)

    log.info('{} skus are fetched from {} keywords'.format(len(skus), len(keywords)))
    check_unpublish_products(keywords, skus)

def check_product(product):
    sku = product['sku']
    product_prev = database.document('hermes_us_product', sku).get().to_dict()

    if not product_prev:
        # Insert the product into the database if not exists
        create_product(product)
        mailer.send_email(product, 'published', product['updated_at'])
    elif not product_prev['published']:
        update_product_by_product(product, product_prev)
        mailer.send_email(product, 'republished', product['updated_at'])

def create_product(product):
    timestamp = product['updated_at']

    product['created_at'] = timestamp
    product['last_published_at'] = timestamp
    product['historical_publish'] = [{
        'publish': True,
        'timestamp': timestamp,
    }]
    product['published'] = True

    database.udpate_product_to_database(product, merge=False) 

def update_product_by_product(product, product_prev):
    timestamp = product['updated_at']
    is_publish = product['published']

    if is_publish:
        product['last_published_at'] = timestamp

    product['historical_publish'] = product_prev['historical_publish']
    if is_publish != product_prev['published']:
        product['historical_publish'].append({
            'publish': is_publish,
            'timestamp': timestamp,
        })

    database.udpate_product_to_database(product, merge=False)

def update_product_publish_by_sku(sku, product_prev, is_publish):
    timestamp = datetime.now(pytz.timezone('US/Pacific'))
    product = {
        'sku': sku,
        'updated_at': timestamp,
        'historical_publish': product_prev['historical_publish'],
        'published': is_publish,
    }

    if is_publish:
        product['last_published_at'] = timestamp

    if is_publish != product_prev['published']:
        product['historical_publish'].append({
            'publish':  is_publish,
            'timestamp': timestamp,
        })

    database.udpate_product_to_database(product, merge=True)

def check_unpublish_products(keywords, skus):
    timestamp = datetime.now(pytz.timezone('US/Pacific'))
    published_products_docs = database.collection('hermes_us_product').where('published', '==', True).stream()
    for doc in published_products_docs:
        product_prev = doc.to_dict()
        if product_prev['keyword'] not in keywords:
            continue
        sku = product_prev['sku']
        if sku not in skus:
            update_product_publish_by_sku(sku, product_prev, False)
            mailer.send_email(product_prev, 'unpublished', timestamp)

if __name__ == '__main__':
    main()
