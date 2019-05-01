import itertools
from django.conf import settings

import django_tables2 as tables

from .models import (
    Link,
    Product,
    Inventory,
    SchedulerLookUp,
    SchedulerRecord,
    TypeLinkRecord,
    BestProduct
)

class LinkTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    link = tables.TemplateColumn('<a href="{% url "links:type-link-product-list" record.pk %}" data-id="{{record.pk}}">{{ record.link }}</a>')

    class Meta:
        model = Link
        exclude = [
            'id',
            'key',
            'sub_key',
            'created',
            'updated'
        ]
        attrs = {
            'class': 'table table-striped table-bordered table-scroll',
        }
        sequence = ['row_number', 'link',]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)


class ProductTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    name = tables.TemplateColumn('<a href="{% url "links:type-link-inventory-list" record.pk %}">{{ record.name }}</a>')
    pub = tables.Column(empty_values=(), verbose_name='PUB', orderable=False)
    # link = tables.TemplateColumn('<a href="{{record.link}}">{{ record.link|truncatechars:40 }}</a>')
    link = tables.TemplateColumn('<a href="{{record.link}}">{{ record.link }}</a>')
    view = tables.TemplateColumn('''
        <div class="btn-block" data-id="{{record.pk}}">
            <a href="#" class="btn btn-xs" title="Edit" id="chart">
                <i class="fa fa-eye"></i>
            </a>
        </div>
    ''', orderable=False)

    class Meta:
        model = Product
        exclude = [
            'id',
            'identity',
            'updated',
        ]
        attrs = {
            'class': 'table table-striped table-bordered table-scroll',
        }
        sequence = ['row_number', 'name', 'view', 'pub', ]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    def render_pub(self, record):
        return f'{record.link.pub}'


class BestProductTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    created = tables.TemplateColumn('<a href="{% url "links:best-product-detail" record.pk %}" data-id="{{record.pk}}">{{ record }}</a>')

    class Meta:
        model = BestProduct
        exclude = [
            'id',
            'updated',
        ]
        attrs = {
            'class': 'table table-striped table-bordered',
        }
        sequence = ['row_number', 'created',]
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


class ScraperRecordTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)

    class Meta:
        model = SchedulerLookUp
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


class SchedulerRecordTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    name = tables.TemplateColumn('<a href="{% url "links:scheduler-record-detail" record.id %}">{{record.name}}</a>')
    links = tables.Column(empty_values=(), verbose_name='Links', orderable=False)

    class Meta:
        model = SchedulerRecord
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

    def render_links(self, record):
        return '%d' % (record.links.count())

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)


class TypeLinkRecordTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    links = tables.TemplateColumn('''
        <a href="{% url "links:type-link-history-detail" record.id %}">{{record.link_set.count}}</a>
    ''', orderable=False)

    class Meta:
        model = TypeLinkRecord
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


class CommaFeedLinkTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    link = tables.TemplateColumn('<a href="{% url "links:type-link-product-list" record.pk %}" data-id="{{record.pk}}">{{ record.link }}</a>')

    class Meta:
        model = Link
        exclude = [
            'id',
            'key',
            'sub_key',
            'created',
            'updated',
            'pub',
            'insert',
            'state',
            'deprecated',
        ]
        attrs = {
            'class': 'table table-striped table-bordered',
        }
        sequence = ['row_number', 'link',]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)
