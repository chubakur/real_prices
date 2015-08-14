from django.core.management import BaseCommand
from .. import Shop
import argparse


class Command(BaseCommand):
    help = "Load price for chosen shop from csv file"

    def add_arguments(self, parser):
        parser.add_argument('shop_id', type=int)
        parser.add_argument('csv_file', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        print args, options
