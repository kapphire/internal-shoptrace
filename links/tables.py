import itertools
from django.conf import settings
from django.utils import timezone

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


class SpecialProductTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="#", orderable=False)
    name = tables.TemplateColumn('<a href="{% url "links:type-link-inventory-list" record.pk %}">{{ record.name }}</a>')
    # pub = tables.Column(empty_values=(), verbose_name='PUB', orderable=False)
    # link = tables.TemplateColumn('<a href="{{record.link}}">{{ record.link|truncatechars:40 }}</a>')
    # link = tables.TemplateColumn('<a href="{{record.link}}">{{ record.link }}</a>')
    last_refreshed = tables.Column(empty_values=(), verbose_name="Last Refreshed Time", orderable=False)
    hour_6 = tables.Column(empty_values=(), verbose_name="0-6h Day to day", orderable=False)
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
            'pub',
            'identity',
            'updated',
        ]
        attrs = {
            'class': 'table table-striped table-bordered table-scroll',
        }
        sequence = [
            'row_number',
            'name',
            'created',
            'view',
            'last_refreshed',
            'hour_6'
        ]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.counter = itertools.count()
        self.today = timezone.now().date()
        self.yesterday = timezone.now() - timezone.timedelta(days=1)
        self.before = timezone.now() - timezone.timedelta(days=2)

    def get_today_inventories(self, record):
       return record.inventory_set.filter(created__gte=self.yesterday)

    def get_day_before_inventories(self, record):
        return record.inventory_set.filter(created__gte=self.before, created__lte=self.today)

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    # def render_pub(self, record):
    #     return f'{record.link.pub}'

    def render_last_refreshed(self, record):
        inventory = record.inventory_set.all().last()
        return inventory.created.strftime('%m/%d/%Y %H:%M')

    def render_hour_6(self, record):
        print('================')
        today_s = self.get_today_inventories(record)
        yesterday_s = self.get_day_before_inventories(record)        
        if today_s and yesterday_s and today_s[1] and today_s[0] and yesterday_s[0] and yesterday_s[1]:
            return (today_s[1].qty - today_s[0].qty) - (yesterday_s[1].qty - yesterday_s[0].qty)
        return 'NaN'


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
