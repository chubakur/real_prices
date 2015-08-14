from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "test command"

    def handle(self, *args, **options):
        print "hello command"