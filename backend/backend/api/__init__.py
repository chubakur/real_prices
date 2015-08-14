__author__ = 'chubakur'
from json import dumps
from django.http import HttpResponse
from ..models import Shop, Product, Price
from itertools import chain


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


@custom_headers
def products_in_shop(requst):
    if 'shop_id' not in requst.GET:
        return HttpResponse(dumps({'error': 'shop_id required'}))
    _products = Product.objects.filter(shop=int(requst.GET['shop_id']))
    # products_view = [o.data() for o in _products]
    # for product_view in products_view:
    #     product_view['prices'] = [p.data() for p in Price.objects.filter(product=o).order_by('-created')]
    # return HttpResponse(dumps(products_view), content_type='application/json')
    return HttpResponse(dumps([dict(chain(o.data().items(),
                                          [('prices',
                                            [p.data() for p in Price.objects.filter(product=o).order_by('-created')])]
                                          )) for o in _products]), content_type="application/json")


@custom_headers
def find_product_by_url(request):
    if 'query' not in request.GET:
        return HttpResponse(dumps({'error': 'query required'}))
    else:
        return HttpResponse(dumps([]))