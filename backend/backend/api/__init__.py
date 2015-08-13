__author__ = 'chubakur'
from json import dumps
from django.http import HttpResponse
from ..models import Shop


def shops(request):
    _shops = Shop.objects.all()
    return HttpResponse([o.data() for o in _shops])
