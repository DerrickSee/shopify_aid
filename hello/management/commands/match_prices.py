import requests
import math

from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from annoying.functions import get_object_or_None

from hello.models import *


class Command(BaseCommand):
    help = 'Match vendor products to products'

    def handle(self, *args, **options):
        upholstery = ProductType.objects.filter(title__in=('sofas', 'loveseats', 'accent chairs', 'sofa chairs', 'daybeds', 'living room sets', 'ottomans', 'recliners', 'sectionals', 'sofa chaises'))
        vendors = Vendor.objects.filter(title__in=('Ashley', 'United', 'Jonathan Louis', 'Istikbal'))
        for vendor in Vendor.objects.all():
            for product in Product.objects.filter(vendor=vendor):
                skus = product.sku.strip("'")
                skus = skus.split('+')
                cost_price = Decimal('0.00')
                all_accounted = True
                for sku in skus:
                    sku = sku.split('*')
                    vp = get_object_or_None(VendorProduct, vendor=vendor, sku=sku[0])
                    try:
                        qty = sku[1]
                    except:
                        qty = '1'
                    if vp:
                        cost_price += vp.price * Decimal(qty)
                    else:
                        all_accounted = False
                if all_accounted:
                    product.cost_price = cost_price
                    if product.product_type in upholstery and product.vendor in vendors:
                        product.retail_price = cost_price * Decimal('3.57')
                    else:
                        product.retail_price = cost_price * Decimal('3.25')
                    sale_price = product.retail_price * Decimal('0.7')
                    if sale_price <= 200:
                        sale_price = math.ceil(sale_price) - 0.01
                    else:
                        if sale_price % 100  < 50:
                            sale_price = math.floor(sale_price / 100) * 100 + 49.99
                        else:
                            sale_price = math.ceil(sale_price / 100) * 100 - 0.01
                    product.sale_price = sale_price
                    product.save()
                    print '%s updated' % product.sku
                else:
                    print '%s skipped' % product.sku

        print 'Price Matched'
