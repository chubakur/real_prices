from django.core.management import BaseCommand
import grequests

urls = ['https://api.import.io/store/connector/19da878e-c84a-4a42-95ae-d973231668a0/_query?input=webpage/url:http://www.velodrive.ru/bicycles/author/author_aura_22_2015.html&_apikey=fe765d477b3c48969c03df4162093f56a0ad52109444b9d22c63b1edae2b21288f52304ec2e6ff8cf068e9cc08b534b20bd9886b19de85f9d5440918918c0e952bf627b82f569925663ba48804144be6',
        'https://api.import.iod/store/connector/19da878e-c84a-4a42-95ae-d973231668a0/_query?input=webpage/url:http://www.velodrive.ru/bicycles/author/author_aura_22_2215.html&_apikey=fe765d477b3c48969c03df4162093f56a0ad52109444b9d22c63b1edae2b21288f52304ec2e6ff8cf068e9cc08b534b20bd9886b19de85f9d5440918918c0e952bf627b82f569925663ba48804144be6'
        ]

class Command(BaseCommand):
    def handle(self, *args, **options):
        rs = (grequests.get(url) for url in urls)
        a = grequests.map(rs)
        for i in a:
            if i:
                print i.json()
