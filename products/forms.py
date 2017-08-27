# from django import forms
# from .models import Product
#
# class ProductAddForm(forms.Form):
#     name = models.CharField(max_length=150)
#     description = models.CharField(max_length=1000)
#     category = models.CharField(max_length=10)
#     price = models.DecimalField(max_digits=7, decimal_places=2, default=2.99,
#         validators=[MinValueValidator(1)])
#     sale_price = models.DecimalField(max_digits=7, decimal_places=2,
#         default=price, blank=True, null=True, validators=[MinValueValidator(1)])
#     shipping_weight = models.DecimalField(max_digits=5, decimal_places=2,
#         default=0.05, validators=[MinValueValidator(0.00)])
#
# class ProductUpdateForm(forms.Form):
#     name = models.CharField(max_length=150)
#     category = models.CharField(max_length=50)
#     description = models.CharField(max_length=1000)
#     price = models.DecimalField(max_digits=7, decimal_places=2, default=2.99,
#         validators=[MinValueValidator(1)])
#     sale_price = models.DecimalField(max_digits=7, decimal_places=2,
#         default=price, blank=True, null=True, validators=[MinValueValidator(1)])
#     shipping_weight = models.DecimalField(max_digits=5, decimal_places=2,
#         default=0.05, validators=[MinValueValidator(0.00)])
#
#     class Meta:
#         model = Product
#         fields = [
#             "name",
#             "category",
#             "description",
#             "price",
#             "sale_price",
#             "shipping_weight"
#         ]
