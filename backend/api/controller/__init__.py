__author__ = 'chubakur'
from json import dumps
from django.http import HttpResponse
from ..models import Shop, Product, Price


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
def products_in_shop(request):
    if 'shop_id' not in request.GET or 'query' not in request.GET:
        return HttpResponse(dumps({'error': 'shop_id and query are required'}))
    _products = Product.objects.filter(shop=int(request.GET['shop_id']), name__icontains=request.GET['query'])
    return HttpResponse(dumps([product.data() for product in _products]), content_type="application/json")


@custom_headers
def history_prices(request):
    if 'product_id' not in request.GET:
        return HttpResponse(dumps({'error': 'product_id is required'}))
    prices = Price.objects.filter(product=int(request.GET['product_id'])).order_by('-created')
    return HttpResponse(dumps([price.data() for price in prices]), content_type="application/json")


@custom_headers
def find_product_by_url(request):
    if 'query' not in request.GET:
        return HttpResponse(dumps({'error': 'query required'}))
    else:
        return HttpResponse(dumps([]))