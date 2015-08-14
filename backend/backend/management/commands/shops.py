from django.core.management import BaseCommand
from .. import Shop


class Command(BaseCommand):
    help = "Display all shops and their IDS from current database"

    def handle(self, *args, **options):
        for i in Shop.objects.all():
            print unicode(i), i.id

