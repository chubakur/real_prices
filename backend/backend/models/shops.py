from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    logo = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def data(self):
        return {'name': self.name,
                'description': self.description,
                'url': self.url,
                'logo': self.logo}
