import requests

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from hello.models import Vendor, VendorData, VendorProduct


class Command(BaseCommand):
    help = 'Update coaster prices'

    def handle(self, *args, **options):

        vendor, created = Vendor.objects.get_or_create(title='Coaster')
        vd, created = VendorData.objects.get_or_create(vendor=vendor, date=now().date())
        url = "http://api.coasteramer.com/api/product/GetPriceList"
        headers = {'keycode': 'ED10E97E26A24442B4526F74D7'}
        response = requests.get(url, headers=headers)
        vd.prices = response.json()
        vd.save()

        for obj in vd.prices:
            if obj['PriceCode'] == 'PR-2034':
                prices = obj['PriceList']
                break
        for price in prices:
            product, created = VendorProduct.objects.update_or_create(
                vendor=vendor, sku=price['ProductNumber'], defaults={'price': Decimal(price['Price'])})
        print 'Data saved'
