from django.core.management import BaseCommand
from .. import Product
from .. import settings
import logging
from . import str_to_number
import traceback
from multiprocessing import Pool
import requests

logger_name = 'UPDATE_PRICES'


logger = logging.getLogger(logger_name)
handler = logging.FileHandler("%s.log" % logger_name)
handler.setFormatter(logging.Formatter('%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

api_addr = 'https://api.import.io'


def create_query_url(connector_id, url):
    return "%s/store/connector/%s/_query?_apikey=%s&input=webpage/url:%s" % \
           (api_addr, connector_id, settings.IMPORTIO['key'], url)


def updater(product):
    product.in_queue = True
    request_url = create_query_url(product.shop.crawler_id, product.url)
    return_result = [product]
    try:
        response = requests.get(request_url)
        parsed_response = response.json()
        if 'error' in parsed_response:
            logger.warning("ErrorInJson:%s:%s" % (parsed_response['error'], request_url))
            if parsed_response['errorType'] == 'NotFoundException':
                product.not_found = True
            else:
                product.in_queue = False
        elif parsed_response['results']:
            result = parsed_response['results'][0]
            if result['price'] and result['price2']:
                new_price = product.update_price((str_to_number(result['price']),
                                                  str_to_number(result['price2'])))
                if new_price:
                    return_result.append(new_price)

        else:
            logger.warning("EmptyResults:%s:%s" % (response.text, request_url))
    except requests.ConnectionError:
        product.in_queue = False
        logger.error("ConnectionError:%s" % request_url)
    finally:
        return return_result


class Command(BaseCommand):

    help = "Update prices of existed products"

    def add_arguments(self, parser):
        parser.add_argument('package_size', type=int)
        parser.add_argument('--thread_count', type=int, default=8)

    def get_random_products(self, package_size):
        return Product.objects.filter(in_queue=False).order_by('?')[0:package_size]

    def handle(self, *args, **options):
        Product.objects.all().update(in_queue=False)
        package_size = options['package_size']
        total = 0
        print options['thread_count']
        while True:
            products = self.get_random_products(package_size)
            print "\r%d" % total,
            pool = Pool(options['thread_count'])
            changed_objects = pool.map(updater, [product for product in products])
            for changed_object in changed_objects:
                for c in changed_object:
                    c.save()

            total += len(products)
            if not products:
                break
