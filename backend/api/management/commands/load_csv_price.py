from django.core.management import BaseCommand
from .. import Shop, Product, Price
import argparse
import csv
from . import str_to_number


class Command(BaseCommand):
    help = "Load price for chosen shop from csv file"

    def add_arguments(self, parser):
        parser.add_argument('shop_id', type=int)
        parser.add_argument('csv_file', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        selected_shop = Shop.objects.get(pk=options['shop_id'])
        print unicode(selected_shop)
        reader = csv.DictReader(options['csv_file'])
        new_products = 0
        new_prices = 0
        for i in reader:
            product, created = Product.objects.get_or_create(url=i['_pageUrl'], defaults={
                'name': i['name'],
                'logo': i['logo'],
                'description': i['description'],
                'shop': selected_shop
            })
            if created:
                new_products += 1
            last_price = Price.objects.filter(product=product).order_by('-created')[0:1]
            if not last_price \
                    or last_price[0].price != str_to_number(i['price'])\
                    or last_price[0].price2 != str_to_number(i['price2']):
                new_price = Price(product=product, price=str_to_number(i['price']), price2=str_to_number(i['price2']))
                new_prices += 1
                new_price.save()
        print "New products:", new_products
        print "New prices:", new_prices

