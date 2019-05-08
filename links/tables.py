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
    link = tables.TemplateColumn('<a href="{{record.link}}">{{ record.link }}</a>')
    last_refreshed = tables.Column(empty_values=(), verbose_name="Last Refreshed Time", orderable=False)
    hour_6 = tables.Column(empty_values=(), verbose_name="0-6h", orderable=False)
    hour_6_comparison = tables.Column(empty_values=(), verbose_name="6h comparison with previous day", orderable=False)
    hour_12 = tables.Column(empty_values=(), verbose_name="0-12h", orderable=False)
    hour_12_comparison = tables.Column(empty_values=(), verbose_name="12h comparison with previous day", orderable=False)
    hour_18 = tables.Column(empty_values=(), verbose_name="0-18h", orderable=False)
    hour_18_comparison = tables.Column(empty_values=(), verbose_name="18h comparison with previous day", orderable=False)
    # hour_24 = tables.Column(empty_values=(), verbose_name="0-24h", orderable=False)
    # hour_24_comparison = tables.Column(empty_values=(), verbose_name="24h comparison with previous day", orderable=False)
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
            'vendor',
            'identity',
            'updated',
            # 'link',
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
            'hour_6',
            'hour_6_comparison',
            'hour_12',
            'hour_12_comparison',
            'hour_18',
            'hour_18_comparison',
            'link',
        ]
        empty_text = "..."

    def __init__(self, *args, **kwargs):
        self.current_parent = kwargs.pop('current_parent')
        super().__init__(**kwargs)
        self.counter = itertools.count()
        self.today = self.current_parent.created.date()
        self.yesterday = (self.current_parent.created - timezone.timedelta(days=1)).date()

    def get_today_inventories(self, record):
        return record.inventory_set.filter(created__gte=self.today).order_by('created')

    def get_day_before_inventories(self, record):
        return record.inventory_set.filter(created__gte=self.yesterday, created__lte=self.today).order_by('created')

    def get_hour_interval(self, record, start):
        data = dict()
        inventories = self.get_today_inventories(record)
        if inventories.exists():
            for i in inventories:
                hour = i.created.hour
                if hour >= start and hour < (start + 6):
                    data['start'] = i
                    continue
                if hour >= (start + 6) and hour < (start + 12):
                    data['end'] = i
                    continue
            if data.get('start') and data.get('end'):
                sale = data['start'].qty - data['end'].qty
                if sale >= 0:
                    return sale
                return 0
        return 'NaN'

    def get_hour_6(self, record):
        return self.get_hour_interval(record, 0)

    def get_hour_12(self, record):
        interval_6 = self.get_hour_6(record)
        interval_12 = self.get_hour_interval(record, 6)
        if not isinstance(interval_6, int) and not isinstance(interval_12, int):
            return 'NaN'
        if not isinstance(interval_6, int):
            interval_6 = 0
        if not isinstance(interval_12, int):
            interval_12 = 0
        return interval_6 + interval_12

    def get_hour_18(self, record):
        interval_12 = self.get_hour_12(record)
        interval_18 = self.get_hour_interval(record, 12)
        if not isinstance(interval_12, int) and not isinstance(interval_18, int):
            return 'NaN'
        if not isinstance(interval_12, int):
            interval_12 = 0
        if not isinstance(interval_18, int):
            interval_18 = 0
        return interval_12 + interval_18

    def get_hour_24(self, record):
        interval_18 = self.get_hour_18(record)
        interval_24 = self.get_hour_interval(record, 18)
        if not isinstance(interval_18, int) and not isinstance(interval_24, int):
            return 'NaN'
        if not isinstance(interval_18, int):
            interval_18 = 0
        if not isinstance(interval_24, int):
            interval_24 = 0
        return interval_18 + interval_24

    def get_day_before_hour_interval(self, record, start):
        data = dict()
        inventories = self.get_day_before_inventories(record)
        if inventories.exists():
            for i in inventories:
                hour = i.created.hour
                if hour >= start and hour < (start + 6):
                    data['start'] = i
                    continue
                if hour >= (start + 6) and hour < (start + 12):
                    data['end'] = i
                    continue
            if data.get('start') and data.get('end'):
                sale = data['start'].qty - data['end'].qty
                if sale > 0:
                    return sale
                return 0
        return 'NaN'

    def get_day_before_hour_6(self, record):
        return self.get_day_before_hour_interval(record, 0)

    def get_day_before_hour_12(self, record):
        interval_6 = self.get_day_before_hour_6(record)
        interval_12 = self.get_day_before_hour_interval(record, 6)
        if not isinstance(interval_6, int) and not isinstance(interval_12, int):
            return 'NaN'
        if not isinstance(interval_6, int):
            interval_6 = 0
        if not isinstance(interval_12, int):
            interval_12 = 0
        return interval_6 + interval_12

    def get_day_before_hour_18(self, record):
        interval_12 = self.get_day_before_hour_12(record)
        interval_18 = self.get_day_before_hour_interval(record, 12)
        if not isinstance(interval_12, int) and not isinstance(interval_18, int):
            return 'NaN'
        if not isinstance(interval_12, int):
            interval_12 = 0
        if not isinstance(interval_18, int):
            interval_18 = 0
        return interval_12 + interval_18

    def get_day_before_hour_24(self, record):
        interval_18 = self.get_day_before_hour_18(record)
        interval_24 = self.get_day_before_hour_interval(record, 18)
        if not isinstance(interval_18, int) and not isinstance(interval_24, int):
            return 'NaN'
        if not isinstance(interval_18, int):
            interval_18 = 0
        if not isinstance(interval_24, int):
            interval_24 = 0
        return interval_18 + interval_24


    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    # def render_pub(self, record):
    #     return f'{record.link.pub}'

    def render_last_refreshed(self, record):
        inventory = record.inventory_set.all().last()
        return inventory.created.strftime('%m/%d/%Y %H:%M')

    def render_hour_6(self, record):
        return self.get_hour_6(record)

    def render_hour_6_comparison(self, record):
        today = self.get_hour_6(record)
        if today == 0:
            return '0 %'
        before = self.get_day_before_hour_6(record)

        if isinstance(today, int) and isinstance(before, int):
            try:
                return f'{round((today - before) / before * 100, 2)}%'
            except:
                return f'{(today - before) / 1 * 100}%'
        return 'NaN'

    def render_hour_12(self, record):
        return self.get_hour_12(record)

    def render_hour_12_comparison(self, record):
        today = self.get_hour_12(record)
        if today == 0:
            return '0 %'
        before = self.get_day_before_hour_12(record)

        if isinstance(today, int) and isinstance(before, int):
            try:
                return f'{round((today - before) / before * 100, 2)}%'
            except:
                return f'{(today - before) / 1 *100}%'
        return 'NaN'

    def render_hour_18(self, record):
        return self.get_hour_18(record)

    def render_hour_18_comparison(self, record):
        today = self.get_hour_18(record)
        if today == 0:
            return '0 %'
        before = self.get_day_before_hour_18(record)

        if isinstance(today, int) and isinstance(before, int):
            try:
                return f'{round((today - before) / before * 100, 2)}%'
            except:
                return f'{(today - before) / 1 *100}%'
        return 'NaN'

    # def render_hour_24(self, record):
    #     return self.get_hour_24(record)

    # def render_hour_24_comparison(self, record):
    #     today = self.get_hour_24(record)
    #     before = self.get_day_before_hour_24(record)

    #     if isinstance(today, int) and isinstance(before, int):
    #         try:
    #             return f'{round((today - before) / before * 100, 2)}%'
    #         except:
    #             return f'{(today - before) / 1 *100}%'
    #     return 'NaN'


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
