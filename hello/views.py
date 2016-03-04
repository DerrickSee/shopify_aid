# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
import csv
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView
from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.text import slugify
from django.utils.timezone import now

from annoying.functions import get_object_or_None

from .names import *
from .models import *

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}
    # context = {'products': Product.objects.all()}
    return render(request, 'index.html', context)


class FileForm(forms.Form):
    file = forms.FileField()


class UploadFormView(FormView):
    form_class = FileForm
    success_url = reverse_lazy('index')
    template_name = "index.html"


class AshleyTableProcess(UploadFormView):

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        writer = csv.writer(response)
        data = [row for row in csv.reader(
                form.cleaned_data['file'].read().splitlines())]
        writer.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name',
                         'Option1 Value', 'Option2 Name', 'Option2 Value','Option3 Name', 'Option3 Value',
                         'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                         'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                         'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable',
                         'Variant Barcode', 'Image Src', 'Image Alt Text',])
        for idx, row in enumerate(data[2:]):
            if row[0]:
                tags = row[2]
                typ = 'mattress'
                vendor = row[0].title()
                name = row[1]
                title = "%s %s %s" % (name, tags,typ)

                handle = slugify(title)
                body = "<p></p><p><strong>DIMENSIONS</strong></p>"
                wholesale = Decimal(row[4].replace('$', '').strip())
                compare = wholesale * Decimal('3.25')
                price = compare * Decimal('0.7')
                writer.writerow([handle, title.title(), body.strip().encode('ascii','ignore'), vendor, typ, tags, "FALSE",
                                 "Color" if row[2] else 'Title', row[2] if row[2] else 'Default Title', "Sleeper" if row[10] else '', row[10] if row[10] else "",
                                 "", "", row[0], "0", "", "0", "continue", "manual", str(price.quantize(Decimal('.01'))),
                                 str(compare.quantize(Decimal('.01'))), "TRUE", "TRUE"])

        return response


class GlobalUInitialProcess(UploadFormView):
    form_class = FileForm
    success_url = reverse_lazy('index')
    template_name = "index.html"

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        writer = csv.writer(response)
        names = []
        data = [row for row in csv.reader(
                form.cleaned_data['file'].read().splitlines())]
        writer.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name',
                         'Option1 Value', 'Option2 Name', 'Option2 Value','Option3 Name', 'Option3 Value',
                         'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                         'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                         'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable',
                         'Variant Barcode', 'Image Src', 'Image Alt Text',])
        for idx, row in enumerate(data[1:]):
            for obj in SWISS:
                name = slugify(obj['surname'].lower())
                if name in names:
                    name = slugify(obj['name'].lower())
                if name not in names:
                    names.append(name)
                    break
            if row[1].lower() == 'sofa':
                types = [('sofa', 'S'), ('loveseat', 'L'), ('sofa chair', 'C'), ('living room set', 'S+L'), ('living room set', 'S+L+C')]
            elif row[1].lower() == 'sectional':
                types = [('sectional', '')]
            tags = [row[2], 'modern']
            colors = row[3].strip(' ').split(',')
            for color in colors:
                tags += [color.lower()]
            if tags[0] in ('bonded leather', 'match leather', 'leather gel'):
                tags += ['faux leather']
            tags = ','.join(tags)
            prices = row[5].split(',')
            widths = row[6].split(',')
            depths = row[7].split(',')
            heights = row[8].split(',')
            for i, typ in enumerate(types):
                body = "<p><strong>DIMENSIONS</strong></p>"
                if i < 3:
                    body += '<p>%s"W x %s"D x %s"H</p>' % (widths[i], depths[i], heights[i])
                else:
                    for ii in (0,1,2):
                        body += '<p>%s - %s"W x %s"D x %s"H</p>' % (types[ii][0].title(), widths[ii], depths[ii], heights[ii])

                skus = row[4].split(',')
                sku = row[0]
                label = '{0} {1}'.format(name, typ[0])
                for num, color in enumerate(colors):
                    sku = row[0]
                    if skus[0] != '':
                            sku += '-%s' % skus[num].strip()
                    if typ[1]:
                        sku += '-%s' % typ[1]
                    handle = 'global-' + slugify(label.lower())
                    wholesale = Decimal(str(prices[i]))
                    compare = wholesale * Decimal('3.25')
                    price = compare * Decimal('0.7')

                    if i < 3:
                        v2 = ''
                    elif i == 3:
                        v2 = 'Sofa & Loveseat'
                    elif i == 4:
                        v2 = 'Sofa, Loveseat & Chair'

                    writer.writerow([handle, label.title(),
                                     body, 'Global', typ[0], tags, 'FALSE',
                                     'Color' if len(colors) > 1 else 'Title',
                                     color.title().strip() if len(colors) > 1 else 'Default Title',
                                     '' if i < 3 else 'Configuration', v2, '', '', sku,
                                     '0', '', '0', 'continue', 'manual',
                                     str(price.quantize(Decimal('.01'))),
                                     str(compare.quantize(Decimal('.01'))),
                                     'TRUE', 'TRUE'])

        return response


class GlobalBedrooms(UploadFormView):
    form_class = FileForm
    success_url = reverse_lazy('index')
    template_name = "index.html"

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        writer = csv.writer(response)
        names = []
        data = [row for row in csv.reader(
                form.cleaned_data['file'].read().splitlines())]
        writer.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name',
                         'Option1 Value', 'Option2 Name', 'Option2 Value','Option3 Name', 'Option3 Value',
                         'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                         'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                         'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable',
                         'Variant Barcode', 'Image Src', 'Image Alt Text',])
        for idx, row in enumerate(data[1:]):
            for obj in NAMES:
                name = slugify(obj['surname'].lower())
                if name in names:
                    name = slugify(obj['name'].lower())
                if name not in names:
                    names.append(name)
                    break
            if row[1].lower() == 'sofa':
                types = [('sofa', 'S'), ('loveseat', 'L'), ('sofa chair', 'C'), ('living room set', 'S+L'), ('living room set', 'S+L+C')]
            elif row[1].lower() == 'sectional':
                types = [('sectional', '')]
            tags = [row[2], 'modern']
            colors = row[3].strip(' ').split(',')
            for color in colors:
                tags += [color.lower()]
            if tags[0] in ('bonded leather', 'match leather', 'leather gel'):
                tags += ['faux leather']
            tags = ','.join(tags)
            prices = row[5].split(',')
            widths = row[6].split(',')
            depths = row[7].split(',')
            heights = row[8].split(',')
            for i, typ in enumerate(types):
                body = "<p><strong>DIMENSIONS</strong></p>"
                if i < 3:
                    body += '<p>%s"W x %s"D x %s"H</p>' % (widths[i], depths[i], heights[i])
                else:
                    for ii in (0,1,2):
                        body += '<p>%s - %s"W x %s"D x %s"H</p>' % (types[ii][0].title(), widths[ii], depths[ii], heights[ii])

                skus = row[4].split(',')
                sku = row[0]
                label = '{0} {1}'.format(name, typ[0])
                for num, color in enumerate(colors):
                    sku = row[0]
                    if skus[0] != '':
                            sku += '-%s' % skus[num].strip()
                    if typ[1]:
                        sku += '-%s' % typ[1]
                    handle = 'global-' + slugify(label.lower())
                    wholesale = Decimal(str(prices[i]))
                    compare = wholesale * Decimal('3.25')
                    price = compare * Decimal('0.7')

                    if i < 3:
                        v2 = ''
                    elif i == 3:
                        v2 = 'Sofa & Loveseat'
                    elif i == 4:
                        v2 = 'Sofa, Loveseat & Chair'

                    writer.writerow([handle, label.title(),
                                     body, 'Global', typ[0], tags, 'FALSE',
                                     'Color' if len(colors) > 1 else 'Title',
                                     color.title().strip() if len(colors) > 1 else 'Default Title',
                                     '' if i < 3 else 'Configuration', v2, '', '', sku,
                                     '0', '', '0', 'continue', 'manual',
                                     str(price.quantize(Decimal('.01'))),
                                     str(compare.quantize(Decimal('.01'))),
                                     'TRUE', 'TRUE'])

        return response


# class CoasterExcel(UploadFormView):
#     form_class = FileForm
#     success_url = reverse_lazy('index')
#     template_name = "index.html"
#
#     def form_valid(self, form):
#         vendor, created = Vendor.objects.get_or_create(title='Coaster')
#         data = [row for row in csv.reader(
#                 form.cleaned_data['file'].read().splitlines())]
#
#         for idx, row in enumerate(data[2:]):
#
#             product, created = Product.objects.update_or_create(
#                 vendor=vendor, sku=row[0],
#                 defaults={'title': row[1], 'description': row[2],
#                           'width': Decimal(row[13] or '0'),
#                           'depth': Decimal(row[14] or '0'),
#                           'height':Decimal(row[15] or '0')})
#         return super(CoasterExcel, self).form_valid(form)


class CoasterProcess(UploadFormView):
    form_class = FileForm
    success_url = reverse_lazy('index')
    template_name = "index.html"

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        writer = csv.writer(response)
        writer.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name',
                         'Option1 Value', 'Option2 Name', 'Option2 Value','Option3 Name', 'Option3 Value',
                         'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                         'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                         'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable',
                         'Variant Barcode', 'Image Src', 'Image Alt Text',])
        vendor, created = Vendor.objects.get_or_create(title='Coaster')
        data = [row for row in csv.reader(
                form.cleaned_data['file'].read().splitlines())]

        for idx, row in enumerate(data[1:]):

            # tags = row[4].lower()
            # if 'fabric' not in tags and 'leather' not in tags:
            #     tags += ',fabric'
            # tags +=',%s' % row[3].lower()
            # colors = row[3].split(',')
        #     for idx, sku in enumerate(row[1].split(',')):
        #
        #         product = Product.objects.get(vendor=vendor, sku=sku.strip())
        #         title = product.title
        #         handle = slugify('%s-' % vendor.title + title)
        #         body = product.description + "<p><strong>DIMENSIONS</strong></p>"
        #         body += '<p>%s"W x %s"D x %s"H</p>'% (product.width, product.depth, product.height)
        #         compare = product.cost_price * Decimal('3.25')
        #         price = compare * Decimal('0.7')
        #         if idx < 1:
        #             tags += ',futon' if product.product_type.title.lower() == 'sofa' else ''
        #         writer.writerow([handle, title, body.encode('ascii','ignore'),
        #                          vendor.title, product.product_type.title.lower(),
        #                          tags, 'FALSE',
        #                          'Color' if len(colors) > 1 else 'Title',
        #                          colors[idx].title().strip() if len(colors) > 1 else 'Default Title',
        #                          '', '', '', '', str(sku.strip()),
        #                          '0', '', '0', 'continue', 'manual',
        #                          str(price.quantize(Decimal('.01'))),
        #                          str(compare.quantize(Decimal('.01'))),
        #                          'TRUE', 'TRUE'])

            # for idx, sku in enumerate(row[1].split(',')):
            #     if sku:
            #         product = get_object_or_None(Product, sku=sku.strip())
            #         handle = slugify('%s-' % vendor.title + product.title)
            #         body = product.description + "<p><strong>DIMENSIONS</strong></p>"
            #         body += '<p>%s"W x %s"D x %s"H</p>'% (product.width, product.depth, product.height)
            #         writer.writerow([handle, product.title, body.encode('ascii','ignore'),
            #                          vendor.title, product.product_type.title.lower(),
            #                          tags, 'FALSE',
            #                          'Color' if len(colors) > 1 else 'Title',
            #                          colors[idx].title().strip() if len(colors) > 1 else 'Default Title',
            #                          '', '', '', '', str(sku.strip()),
            #                          '0', '', '0', 'continue', 'manual',
            #                          str(price.quantize(Decimal('.01'))),
            #                          str(compare.quantize(Decimal('.01'))),
            #                          'TRUE', 'TRUE'])
            if row[2]:

                name = row[0].strip()

                while name == '':
                    res = requests.get('http://uinames.com/api/?region=germany')
                    json = res.json()
                    if not get_object_or_None(Collection, title=slugify(json['name'])):
                        name = slugify(json['name'])
                    elif not get_object_or_None(Collection, title=slugify(json['surname'])):
                        name = slugify(json['surname'])
                collection, created = Collection.objects.get_or_create(title=name.title())
                if 'table' in row[1]:
                    product_type = 'dining table'
                elif 'chair' in row[1]:
                    if 'counter height' in row[1]:
                        product_type = 'barstool'
                    else:
                        product_type = 'side chair'
                else:
                    product_type = row[1].lower().strip()

                title = '%s %s' % (collection.title, product_type)
                product_type, created = ProductType.objects.get_or_create(title=product_type)


                for idx, sku in enumerate(row[2].split(',')):
                    if '+' in sku:
                        product, create = Product.objects.get_or_create(vendor=vendor, sku=sku.strip())
                    else:
                        print sku
                        product = Product.objects.get(vendor=vendor, sku=sku.strip())
                    product.title = title.title()
                    product.product_type = product_type
                    product.collection = collection
                    product.save()
                handle = slugify('%s-' % vendor.title + title)
                body = product.description or ''
                body += "<p><strong>DIMENSIONS</strong></p>"
                body += '<p>%s"W x %s"D x %s"H</p>'% (product.width, product.depth, product.height)
                tags = row[3].lower()
                if 'dinnetes' in tags:
                    tags.strip('dinnetes,')
                    tags += ',dinettes'
                tags +=',%s' % row[4].lower()
                for t in ('counter height', 'round', 'rectangular', 'oval', 'square'):
                    if t in row[1]:
                        tags += ',%s' % t
                colors = row[4].split(',')
                skus = row[2].split(',')
                for idx, sku in enumerate(skus):
                    product = Product.objects.get(vendor=vendor, sku=sku.strip())
                    compare = (product.cost_price or 0) * Decimal('3.25')
                    price = compare * Decimal('0.7')
                    writer.writerow([handle, title, body.encode('ascii','ignore'),
                                     vendor.title, product.product_type.title.lower(),
                                     tags, 'FALSE',
                                     'Color' if len(colors) > 1 else 'Title',
                                     colors[idx].title().strip() if len(skus) > 1 else 'Default Title',
                                     '', '', '', '', str(sku.strip()),
                                     '0', '', '0', 'continue', 'manual',
                                     str(price.quantize(Decimal('.01'))),
                                     str(compare.quantize(Decimal('.01'))),
                                     'TRUE', 'TRUE'])

        return response


def CoasterUpdate():
    vendor = Vendor.objects.get(title='Coaster')
    vd, created = VendorData.objects.get_or_create(vendor=vendor, date=now().date())
    url = "http://api.coasteramer.com/api/product/GetPriceList"
    headers = {'keycode': 'ED10E97E26A24442B4526F74D7'}
    response = requests.get(url, headers=headers)
    vd.prices = response.json()
    vd.save()
    print 'Data saved'


def CoasterPriceCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="processed.csv"'
    writer = csv.writer(response)
    writer.writerow(['SKU', 'Cost 1', 'Cost 2',])
    coaster = Vendor.objects.get(title='Coaster')
    vd = VendorData.objects.get(date=now().date(), vendor=coaster)
    for obj in vd.prices:
        if obj['PriceCode'] == 'PR-2034':
            prices = obj['PriceList']
    for price in prices:
        writer.writerow([price['ProductNumber'], price['Price']])
        product = get_object_or_None(Product, vendor=coaster, sku=price['ProductNumber'])
        if product:
            product.cost_price = Decimal(price['Price'])
            product.save()
    return response


class UpdateCoasterShopifyExport(UploadFormView):
    form_class = FileForm
    success_url = reverse_lazy('index')
    template_name = "index.html"

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        writer = csv.writer(response)

        data = [row for row in csv.reader(
                form.cleaned_data['file'].read().splitlines())]
        writer.writerow(data[0])
        coaster = Vendor.objects.get(title='Coaster')
        for idx, row in enumerate(data[1:]):
            product = get_object_or_None(Product, vendor=coaster, sku=row[13])
            if product and product.cost_price:
                row[20] = (product.cost_price * Decimal('3.25')).quantize(Decimal('.01'))
                row[19] = (product.cost_price * Decimal('3.25') * Decimal('0.7')).quantize(Decimal('.01'))
                if row[24]:
                    row[6] = 'true'
            writer.writerow(row)
        return response


class CleanShopify(UploadFormView):
    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="processed.csv"'
        writer = csv.writer(response)

        data = [row for row in csv.reader(
                form.cleaned_data['file'].read().splitlines())]
        writer.writerow(data[0])
        for idx, row in enumerate(data[1:]):
            if row[1] and row[13]:
                row[6] = 'true' if row[24] else 'false'
            writer.writerow(row)
        return response


def UpdateUsers():
    url = "https://jenniferconvertibles.zendesk.com/api/v2/users.json"
    auth = ('dsee@jenniferfurniture.com', 'kYpcmniLo{8Rm')
    # headers = {'Authorization': 'ED10E97E26A24442B4526F74D7'}
    response = requests.get(url, auth=auth)
    json = response.json()
    for obj in json['users']:
        if obj['email'] and not get_object_or_None(User, email=obj['email']):
            user = User.objects.create_user(obj['email'])
            user.first_name = obj['name'].split(' ')[0]
            user.last_name = obj['name'].split(' ')[-1]
            user.save()
    while json['next_page']:
        response = requests.get(json['next_page'], auth=auth)
        json = response.json()
        for obj in json['users']:
            if obj['email'] and not get_object_or_None(User, email=obj['email']):
                user = User.objects.create_user(obj['email'])
                user.first_name = obj['name'].split(' ')[0]
                user.last_name = obj['name'].split(' ')[-1]
                user.save()
    print 'Users updated'


def ExportUsers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email Address', 'First Name', 'Last Name', 'Email Type'])
    for user in User.objects.all():
        if 'mailer-daemon' in user.email or 'jenniferfurniture' in user.email:
            user.delete()
        else:
            writer.writerow([user.email.encode('ascii','ignore'), user.first_name.encode('ascii','ignore'), user.last_name.encode('ascii','ignore'), 'HTML'])
    return response


def CoasterExcel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name',
                     'Option1 Value', 'Option2 Name', 'Option2 Value','Option3 Name', 'Option3 Value',
                     'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
                     'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                     'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable',
                     'Variant Barcode', 'Image Src', 'Image Alt Text',])
    vendor = Vendor.objects.get(title="Coaster")
    for product in vendor.product_set.filter(title="ART"):
        query = product.description
        stopwords = ['Painting','name:','Name:','Title:','PAINTING','TITLE:']
        querywords = query.split()

        resultwords  = [word for word in querywords if word not in stopwords]
        result = ' '.join(resultwords)

        title = result + ' Wall Art'
        compare = (product.cost_price or 0) * Decimal('3.25')
        price = compare * Decimal('0.7')
        description = '<p>%s</p><p>DIMENSIONS</p>' % product.description.encode('ascii','ignore')
        description += '%s" W x %s" D x %s" H' % (product.width, product.depth, product.height)
        writer.writerow([slugify(title), title.encode('ascii','ignore').title(), description,
                         vendor.title, 'wall art',
                         '', 'FALSE',
                         'Title', 'Default Title',
                         '', '', '', '', str(product.sku.strip()),
                         '0', '', '0', 'continue', 'manual',
                         str(price.quantize(Decimal('.01'))),
                         str(compare.quantize(Decimal('.01'))),
                         'TRUE', 'TRUE'])
    return response
