from django.core.management import BaseCommand
from .. import Product, Shop
from .. import settings
import logging
from . import str_to_number
import traceback
from multiprocessing import Pool
import requests
from functools import partial

logger_name = 'UPDATE_PRICES'


logger = logging.getLogger(logger_name)
handler = logging.FileHandler("%s.log" % logger_name)
handler.setFormatter(logging.Formatter('%(asctime)s %(module)s %(thread)d %(threadName)s %(levelname)s %(lineno)d %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

api_addr = 'https://api.import.io'


def create_query_url(connector_id, url):
    return "%s/store/connector/%s/_query?_apikey=%s&input=webpage/url:%s" % \
           (api_addr, connector_id, settings.IMPORTIO['key'], url)


def updater(crawler_id, product):
    # logger.debug("START UPDATER")
    product.in_queue = True
    request_url = create_query_url(crawler_id, product.url)
    return_result = [product]
    try:
        # logger.debug("START QUERY")
        response = requests.get(request_url, timeout=10)
        # logger.debug("PARSE RESPONSE")
        parsed_response = response.json()
        if 'error' in parsed_response:
            # logger.warning("ErrorInJson:%s:%s" % (parsed_response['error'], request_url))
            if parsed_response['errorType'] == 'NotFoundException':
                product.not_found = True
            else:
                product.in_queue = False
        elif parsed_response['results']:
            # logger.debug("IS OK")
            result = parsed_response['results'][0]
            if result['price'] and result['price2']:
                new_price = product.update_price((str_to_number(result['price']),
                                                  str_to_number(result['price2'])))
                if new_price:
                    return_result.append(new_price)
            # logger.debug("PRICE UPDATED")

        else:
            pass
            # logger.warning("EmptyResults:%s:%s" % (response.text, request_url))
    except requests.ConnectionError:
        product.in_queue = False
        # logger.error("ConnectionError:%s" % request_url)
    except requests.Timeout:
        product.in_queue = False
        # logger.error("Timeout:%s" % request_url)
    except :
        product.in_queue = False
        # logger.error("Error:%s" % traceback.format_exc())
    finally:
        # logger.debug("FINALLY")
        return return_result


def s(a):
    return []


class Command(BaseCommand):

    help = "Update prices of existed products"

    def add_arguments(self, parser):
        parser.add_argument('shop_id', type=int)
        parser.add_argument('package_size', type=int)
        parser.add_argument('--thread_count', type=int, default=8)

    def get_random_products(self, shop, package_size):
        return Product.objects.filter(shop=shop, in_queue=False).order_by('?')[0:package_size]

    def handle(self, *args, **options):
        shop = Shop.objects.get(pk=options['shop_id'])
        print unicode(shop.name)
        Product.objects.filter(shop=shop).update(in_queue=False)
        package_size = options['package_size']
        total = 0
        pool = Pool(options['thread_count'])
        while True:
            print "\r%d" % total,
            products = self.get_random_products(shop, package_size)
            logger.debug("START POOL")
            changed_objects = pool.map(partial(updater, shop.crawler_id), [product for product in products])
            logger.debug("END POOL")
            for changed_object in changed_objects:
                for c in changed_object:
                    c.save()
            logger.debug("END SAVE")

            total += len(products)
            if not products:
                break
