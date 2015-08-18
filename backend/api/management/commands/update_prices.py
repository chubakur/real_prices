from django.core.management import BaseCommand
from .. import settings
from importio import importio, latch
from .. import Shop, Price, Product
from sys import stdout
from . import str_to_number
import logging

logger = logging.getLogger('MSGHDLR')
handler = logging.FileHandler('msg_hdlr.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(module)s %(message)s'))
logger.addHandler(handler)


def create_query(connector_id, url):
    return {'input': {'webpage/url': url}, 'connectorGuids': [connector_id]}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('shop_id', type=int)

    def handle(self, *args, **options):
        selected_shop = Shop.objects.get(pk=options['shop_id'])
        print unicode(selected_shop)
        products = selected_shop.products.all()
        client = importio.importio(user_id=settings.IMPORTIO['guid'], api_key=settings.IMPORTIO['key'])
        client.connect()

        lock = latch.latch(len(products))

        print '%d/%d' % (0, len(products)),
        stdout.flush()

        def callback(query, message):
            if message['type'] == 'MESSAGE':
                if 'pageUrl' in message['data']:
                    _url = message['data']['pageUrl']
                    _product = Product.objects.get(url=_url)
                    result = message['data']['results'][0]
                    price = str_to_number(result['price'])
                    price2 = str_to_number(result['price2'])
                    if _product.price != price or _product.price2 != price2:
                        _new_price = Price(product=_product, price=price,
                                           price2=price2)
                        _product.price = price
                        _product.price2 = price2
                        _product.save()
                        _new_price.save()
                else:
                    logger.error(message)
            if query.finished():
                lock.countdown()
                print '\r%d/%d' % (len(products) - lock.count, len(products)),
                stdout.flush()

        for product in products:
            client.query(create_query(selected_shop.crawler_id, product.url), callback)

        lock.await()
        client.disconnect()



