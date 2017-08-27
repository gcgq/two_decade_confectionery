from django.contrib import admin

from .models import Product
from .models import ProductImage
from .models import Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display= ['name','description','price','sale_price']
    list_filter=['price', 'weight']
    list_editable=['price', 'sale_price']

    search_fields = ['description', 'name']

    class Meta:
        model = Product

class VariationAdmin(admin.ModelAdmin):
    list_display=['__str__', "product"]

class ProductImageAdmin(admin.ModelAdmin):
    list_display=['__str__', "product", "image"]
    list_editable = ["image"]



admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
