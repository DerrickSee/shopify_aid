from celery import Celery
import os
from hello.models import ProductType, Product, Vendor


app = Celery('example')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


@app.task
def add_update_product(row):
    if row[3]:
        title = row[1]
        product_type, created = ProductType.objects.get_or_create(title=row[4])
        vendor = row[3].title()
    try:
        product, created = Product.objects.update_or_create(
            sku=row[13], vendor__title=vendor,
            defaults={'product_type': product_type, 'title': title})
    except:
        vendor, created = Vendor.objects.get_or_create(title=vendor)
        product, created = Product.objects.update_or_create(
            sku=row[13], vendor=vendor,
            defaults={'product_type': product_type, 'title': title})
