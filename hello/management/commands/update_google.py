import requests
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from hello.models import Vendor, VendorData, VendorProduct


class Command(BaseCommand):
    help = 'Update coaster prices'

    def handle(self, *args, **options):

        Product.
        print 'Data saved'
