from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
# from django.core.validators import MinValueValidator
# validators=[MinValueValidator(1)]
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=2.99)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2,
        default=None, blank=True, null=True)
    shipping_weight = models.DecimalField(max_digits=5, decimal_places=2,
        default=0.05)
    slug = models.SlugField(blank=True, default=None)
    active = models.BooleanField( default=True )
    # objects=ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products_slug_view", kwargs={ "slug":self.slug })

def on_product_save(sender, instance, *args, **kwargs):
    # print("on_product_save() parameters: kw: %s, sender: %s, instance: %s" % (**kwargs, sender, instance))
    if not instance.slug:
        print("New slug: ", slugify(instance.name))
        instance.slug = slugify(instance.name)

pre_save.connect(on_product_save, sender=Product)

class Variation(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=150)
    # description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=4.99)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2,
                                     default=None, blank=True, null=True)
    active = models.BooleanField( default=True )
    size = models.DecimalField( decimal_places=0, max_digits=7)

    def __str__(self):
        return self.name

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price

        else:
            return self.price

    def get_absoulute_url(self):
        return self.product.get_absolute_url()

    def add_to_cart(self):
        pass

    def remove_from_cart(self):
        pass

def on_variation_save(sender, instance, *args, **kwargs):
    print("on_variation_save() parameters: sender: {}, instance: {}".format(sender, instance))
    # product = instance
    # variations = product.variation_set.all()

    #create default half-dozen and one dozen variations
    if instance.variation_set.count() == 0:
        half_dozen = Variation(
            product = instance,
            name = "Half-Dozen",
            size = 6,
            price = instance.price * 6,
        )
        half_dozen.save()
        print("Half-Dozen {} created".format( half_dozen.product.name ))

        one_dozen = Variation(
            product = instance,
            name = "One Dozen",
            size = 12,
            price = instance.price * 12,
        )
        one_dozen.save()
        print("One Dozen {} created".format( half_dozen.product.name ))

post_save.connect(on_variation_save, sender=Product)
