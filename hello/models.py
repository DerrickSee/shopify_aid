from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel, TitleDescriptionModel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from taggit.managers import TaggableManager
from jsonfield import JSONField


class Vendor(TitleSlugDescriptionModel):

    class Meta:
        app_label = 'hello'

    def __unicode__(self):
        return self.title


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
    cost_price = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    tags = TaggableManager()

    class Meta:
        app_label = 'hello'


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    objects = MyUserManager()

    class Meta:
        app_label = 'hello'


class VendorData(models.Model):
    products = JSONField(null=True, blank=True)
    prices = JSONField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor)
    date = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'hello'
