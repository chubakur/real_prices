from django.core.management import BaseCommand
from .. import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        for product in Product.objects.all():
            prices = product.prices.all().order_by('-created')
            if prices:
                product.price = prices[0].price
                product.price2 = prices[0].price2
                product.save()
