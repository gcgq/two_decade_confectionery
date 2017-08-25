from django.contrib import admin

from .models import Product
from .models import Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display= ['name','description','price','sale_price']
    list_filter=['price', 'shipping_weight']
    list_editable=['price', 'sale_price']

    search_fields = ['description', 'name']

    class Meta:
        model = Product

class VariationAdmin(admin.ModelAdmin):
    list_display=['__str__', "product"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
# admin.site.register()
