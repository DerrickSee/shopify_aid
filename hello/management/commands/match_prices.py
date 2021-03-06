import requests
import math

from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from annoying.functions import get_object_or_None

from hello.models import *
from hello.constants import GOOGLE_CATEGORIES


class Command(BaseCommand):
    help = 'Match vendor products to products'

    def handle(self, *args, **options):
        upholstery = ProductType.objects.filter(title__in=('sofas', 'loveseats', 'accent chairs', 'sofa chairs', 'daybeds', 'living room sets', 'ottomans', 'recliners', 'sectionals', 'sofa chaises'))
        vendors = Vendor.objects.filter(title__in=('Ashley', 'United', 'Jonathan Louis', 'Istikbal'))
        mattresses = ProductType.objects.filter(title__in=('mattresses', 'box springs'))
        for vendor in Vendor.objects.exclude(title="Guardsman"):
            for product in Product.objects.filter(vendor=vendor):
                skus = product.sku.strip("'")
                skus = skus.split('+')
                cost_price = Decimal('0.00')
                all_accounted = True
                for idx, sku in enumerate(skus):
                    sku = sku.split('*')
                    # @ before *
                    if '@' in sku[0]:
                        ss = sku[0].split('@')
                        vp = get_object_or_None(VendorProduct, vendor__title=ss[1], sku=ss[0])
                    else:
                        vp = get_object_or_None(VendorProduct, vendor=vendor, sku=sku[0])
                    try:
                        qty = sku[1]
                    except:
                        qty = '1'
                    if vp:
                        cost_price += vp.price * Decimal(qty)
                        if idx == 0:
                            product.upc = vp.upc
                            for tt in GOOGLE_CATEGORIES:
                                if product.product_type.title == tt[0]:
                                    product.google_category = tt[1]
                    else:
                        all_accounted = False

                if all_accounted:
                    product.cost_price = cost_price
                    if product.product_type in upholstery and product.vendor in vendors:
                        retail_price = cost_price * Decimal('3.57')
                    else:
                        retail_price = cost_price * Decimal('3.25')
                    if product.product_type in mattresses:
                        sale_price = retail_price * Decimal('0.5')
                    else:
                        sale_price = retail_price * Decimal('0.7')
                    retail_price = math.ceil(retail_price / 10) * 10 - 0.01
                    sale_price = math.ceil(sale_price / 10) * 10 - 0.01
                    # if sale_price <= 200:
                    #     sale_price = math.ceil(sale_price) - 0.01
                    # else:
                    #     if sale_price % 100  < 50:
                    #         sale_price = math.floor(sale_price / 100) * 100 + 49.99
                    #     else:
                    #         sale_price = math.ceil(sale_price / 100) * 100 - 0.01
                    product.retail_price = retail_price
                    product.sale_price = sale_price
                    product.save()
                    print '%s updated' % product.sku
                else:
                    print '%s skipped' % product.sku

        print 'Price Matched'
