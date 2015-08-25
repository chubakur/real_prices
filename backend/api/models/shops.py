from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    url = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    logo = models.CharField(max_length=200, null=True)
    crawler_id = models.CharField(max_length=36, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def data(self):
        return {'name': self.name,
                'description': self.description,
                'url': self.url,
                'logo': self.logo,
                'id': self.id
                }


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True)
    url = models.CharField(max_length=1024)
    logo = models.CharField(max_length=1024, null=True)
    created = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop, related_name='products')
    price = models.FloatField(null=True)
    price2 = models.FloatField(null=True)
    not_found = models.BooleanField(default=False, null=False)
    in_queue = models.BooleanField(default=False, null=False)

    def update_price(self, prices):
        price, price2 = prices
        if price != self.price or price2 != self.price2:
            self.price, self.price2 = price, price2
            return Price(price=price, price2=price2, product=self)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def data(self):
        return {
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'logo': self.logo
        }


class Price(models.Model):
    product = models.ForeignKey(Product, related_name='prices')
    created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    price2 = models.FloatField()

    def __str__(self):
        return u"%s: %d %d" % (unicode(self.product), self.price, self.price2)

    def __unicode__(self):
        return u"1"

    def data(self):
        return {
            'price': self.price,
            'price2': self.price2
        }

