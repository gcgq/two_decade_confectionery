from decimal import Decimal
from django.db import models
from django.conf import settings

from django.views.generic.list import ListView

from django.db.models.signals import pre_save, post_save

from carts.models import Cart
# Create your models here.


class UserCheckout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)
    # merchant_id

    def __str__(self):
        return self.email

    # def get_client_token(self):
    #     customer_id = self.get_braintree_id
    #     if customer_id:
    #         client_token = braintree.ClientToken.generate({
        #           "customer_id": customer_id
        #       })
        #       return client_token
        #   return None


ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)

    def __str__(self):
        return self.street

    def get_address(self):
        return "%s,%s,%s,%s" %(self.street, self.city, self.state, self.zipcode)



ORDER_STATUS_CHOICES= (
        ('created','Created'),
        ('completed','Completed'),
        )
class Order(models.Model):
    status = models.CharField(max_length=120, choices = ORDER_STATUS_CHOICES, default = "created")
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout, null=True)
    billing_address = models.ForeignKey(
        UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(
        UserAddress, related_name='Shipping_address', null=True)
    shipping_total_price = models.DecimalField(
        max_digits=50, decimal_places=2, default=5.99)
    order_total = models.DecimalField(max_digits=50, decimal_places=2, )
    order_total_in_cents = models.IntegerField()
    # order_id

    def __str__(self):
        return str(self.cart.id)

    def mark_completed(self):
        self.status = "completed"
        self.save()

def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + Decimal(cart_total)
    instance.order_total = order_total
    instance.order_total_in_cents = int(order_total*100)

print(pre_save.connect(order_pre_save, sender=Order))