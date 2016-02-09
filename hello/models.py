from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel, TitleDescriptionModel
from taggit.managers import TaggableManager

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Vendor(TitleSlugDescriptionModel):

    class Meta:
        app_label = 'hello'


class Collection(TitleSlugDescriptionModel):

    class Meta:
        app_label = 'hello'


class ProductType(TitleSlugDescriptionModel):

    class Meta:
        app_label = 'hello'


class Product(TitleDescriptionModel):
    sku = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor)
    product_type = models.ForeignKey(ProductType, null=True)
    width = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    depth = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    height = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    collection = models.ForeignKey(Collection, null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        app_label = 'hello'
