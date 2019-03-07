import itertools
from django.conf import settings

import django_tables2 as tables

from .models import Link, Product, Inventory

class LinkTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    link = tables.TemplateColumn('<a href="{% url "links:type-link-product-list" record.pk %}">{{ record.link }}</a>')

    class Meta:
        model = Link
        exclude = [
            'id',
            'created',
            'updated'
        ]
        attrs = {
            'class': 'table table-striped table-bordered table-scroll',
        }
        sequence = ['row_number', ]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)


class ProductTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    name = tables.TemplateColumn('<a href="{% url "links:type-link-inventory-list" record.pk %}">{{ record.name }}</a>')

    class Meta:
        model = Product
        exclude = [
            'id',
        ]
        attrs = {
            'class': 'table table-striped table-bordered',
        }
        sequence = ['row_number', ]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)


class InventoryTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)

    class Meta:
        model = Inventory
        exclude = [
            'id',
        ]
        attrs = {
            'class': 'table table-striped table-bordered',
        }
        sequence = ['row_number', ]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)
