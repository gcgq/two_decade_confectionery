from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# from django.conf import settings
# from django.core.validators import MinValueValidator
# validators=[MinValueValidator(1)]
# Create your models here.

class Product(models.Model):
    TRUFFLE = 'Truffle'
    COOKIE = 'Cookie'
    CUPCAKE = 'Cupcake'
    CATEGORY_CHOICES = (
        (TRUFFLE, 'Truffle'),
        (COOKIE, 'Cookie'),
        (CUPCAKE, 'Cupcake')
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=10,
        choices=CATEGORY_CHOICES, default=TRUFFLE)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=7, decimal_places=2,
        default=2.99)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2,
        default=None, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    available_inventory = models.PositiveIntegerField(default=100)
    slug = models.SlugField(blank=True, default=None)
    active = models.BooleanField(default=True)
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
    price = models.DecimalField(max_digits=7, decimal_places=2,
        default=4.99)
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

    def get_title(self):
        return "{}, {}".format(self.product.name, self.name)

    def get_absoulute_url(self):
        return self.product.get_absolute_url()

    def add_to_cart(self):
        return "{}/?item={}&qty=1".format(reverse("cart"), self.id)

    def remove_from_cart(self):
        return "{}?item={}&qty=1&delete=True".format(reverse("cart"), self.id)

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

def image_upload_to(instance, filename):
    basename, file_extension = filename.split(".")
    new_filename = "{}.{}".format(instance.product.id, file_extension)
    return settings.STATIC_URL + "/products/{}".format(new_filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.name
