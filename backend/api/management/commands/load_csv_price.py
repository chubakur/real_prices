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
            csv_price = str_to_number(i['price'])
            csv_price2 = str_to_number(i['price2'])
            product, created = Product.objects.get_or_create(url=i['_pageUrl'], defaults={
                'name': i['name'],
                'logo': i['logo'],
                'description': i['description'],
                'shop': selected_shop,
                'price': csv_price,
                'price2': csv_price2
            })
            if created:
                new_products += 1
                if product.price != csv_price or product.price2 != csv_price2:
                    new_price = Price(product=product, price=csv_price, price2=csv_price2)
                    product.price = csv_price
                    product.price2 = csv_price2
                    new_prices += 1
                    product.save()
                    new_price.save()
        print "New products:", new_products
        print "New prices:", new_prices

