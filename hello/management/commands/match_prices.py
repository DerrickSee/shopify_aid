import requests
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from hello.models import *


class Command(BaseCommand):
    help = 'Match vendor products to products'

    def add_arguments(self, parser):
        parser.add_argument('vendor', nargs='+', type=str)


    def handle(self, *args, **options):
        upholstery = ProductType.objects.filter(title__in=('sofas', 'loveseats', 'accent chairs', 'sofa chairs', 'daybeds', 'living room sets', 'ottomans', 'recliners', 'sectionals', 'sofa chaises'))
        vendors = Vendor.objects.filter(title__in=('Ashley', 'United', 'Jonathan Louis', 'Istikbal'))
        vendor, created = Vendor.objects.get_or_create(title=options['vendor'])

        for product in Product.objects.filter(vendor=vendor):
            vp = get_object_or_None(VendorProduct, vendor=vendor, sku=product.sku)
            if vp:
                product.cost_price = vp.price
                if product.product_type in upholstery and product.vendor in vendors:
                    product.retail_price = vp.price * Decimal('3.57')
                else:
                    product.retail_price = vp.price * Decimal('3.25')
                product.sale_price = vp.price * Decimal('0.7')
                product.save()

        print 'Price Matched'
