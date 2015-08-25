from django.contrib import admin
from models import Shop, Product, Price


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('shop', 'not_found')
    search_fields = ('name', )

admin.site.register(Shop)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price)
