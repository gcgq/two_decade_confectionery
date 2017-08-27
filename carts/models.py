from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.conf import settings

from products.models import Variation
# Create your models here.

class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.name

    def remove(self):
        return self.item.remove_from_cart()

def on_cartitem_save(sender, instance, *args, **kwargs):
    qty = instance.quantity
    price = instance.item.get_price()
    if int(qty) >= 1:
        instance.line_item_total = Decimal(qty) * Decimal(price)

def after_cartitem_save(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

pre_save.connect(on_cartitem_save, sender=CartItem)
post_delete.connect(after_cartitem_save, sender=CartItem)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variation, through=CartItem)

    tax_percentage = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        print("update total")
        self.subtotal=0
        items = self.cartitem_set.all()
        for item in items:
            self.subtotal += item.line_item_total
        self.save()

def on_cart_save(sender, instance, *args, **kwargs):
    #caluculate tax on cart save
    instance.tax_total = round(instance.subtotal * instance.tax_percentage, 2)
    instance.total = round(instance.subtotal + instance.tax_total, 2)

pre_save.connect(on_cart_save, sender=Cart)
