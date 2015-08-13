__author__ = 'chubakur'
from json import dumps
from django.http import HttpResponse
from ..models import Shop


def custom_headers(fnc):
    def wrapper(*args, **kwargs):
        response = fnc(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = "*"
        return response
    return wrapper


@custom_headers
def shops(request):
    _shops = Shop.objects.all()
    return HttpResponse(dumps([o.data() for o in _shops]), content_type="application/json")
