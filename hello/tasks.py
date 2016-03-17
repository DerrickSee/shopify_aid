import django
django.setup()

from celery import shared_task
from .models import ProductType, Product, Vendor


@shared_task
def add_update_product(data):
    for idx, row in enumerate(data[1:]):
        if row[13]:
            if row[3]:
                title = row[1]
                product_type = row[4]
                vendor = row[3].title()
            try:
                product, created = Product.objects.update_or_create(
                    sku=row[13], vendor__title=vendor,
                    defaults={'title': title})
            except:
                vendor, created = Vendor.objects.get_or_create(title=vendor)
                product_type,created = ProductType.objects.get_or_create(title=product_type)
                product, created = Product.objects.update_or_create(
                    sku=row[13], vendor=vendor,
                    defaults={'product_type': product_type, 'title': title})
