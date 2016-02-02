# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.text import slugify
from decimal import Decimal
from .names import *

import csv

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

class FileForm(forms.Form):
    file = forms.FileField()


class AshleyTableProcess(FormView):
    form_class = FileForm
    success_url = reverse_lazy('index')
    template_name = "index.html"

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
            des = row[8].strip().lower()
            tags = ''
            if des in ('occasional table set', 'square cocktail table', 'rectangular cocktail table', 'oval cocktail table', 'cocktail tbl w/4 stools',
                       'rectangular cocktail', 'round cocktail table', 'storage cocktail tbl', 'cocktail table',
                       'rect. cocktail table', 'lift top cocktail table', 'storage cocktail table', 'storage cocktail chest',
                       'cocktail table with storage', 'cocktail table w/storage', 'octagon cocktail table'):
                typ = "coffee table"
            elif 'end table' in des or des in ('round accent table', 'ends', 'square ends table'):
                typ = "end table"
            elif des in ('console sofa table', 'sofa table', 'console', 'console table'):
                typ = "console table"
            elif des in ('pier cabinet', 'accent cabinet', 'wine rack', 'door accent cabinet', 'accent door cabinet'):
                typ = "cabinet"
            elif des == 'tv stand':
                typ = "tv stand"
            else:
                print des, idx
                continue

            if 'round' in des:
                tags += 'round,'
            elif 'rect' in des:
                tags += 'rectangular,'
            elif 'square' in des:
                tags += 'square,'
            elif 'oval' in des:
                tags += 'oval,'
            elif 'octagon' in des:
                tags += 'octagon,'

            if 'storage' in des:
                tags += 'storage,'
            if 'set' in des:
                tags += 'set,'

            title = row[1].strip() + ' ' + typ
            handle = slugify(title)
            body = "<p>%s</p>" % row[10]
            body += "<p><strong>DIMENSIONS</strong></p>"
            body += "<p>%s</p>" % row[12]
            vendor = "Ashley"
            wholesale = Decimal(row[4].strip('$'))
            compare = wholesale * Decimal('3.25')
            price = compare * Decimal('0.7')
            writer.writerow([handle, title.title(), body, vendor, typ, tags, "FALSE", "", "", "", "",
                             "", "", row[0], "0", "", "0", "continue", "manual", str(price.quantize(Decimal('.01'))),
                             str(compare.quantize(Decimal('.01'))), "TRUE", "TRUE"])


        return response


class GlobalUInitialProcess(FormView):
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


class GlobalBedrooms(FormView):
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
