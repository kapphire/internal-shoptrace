import itertools
from django.conf import settings
from django.utils import timezone

today = timezone.now().date()
yesterday = (timezone.now() - timezone.timedelta(days=1)).date()

def get_today_inventories(record):
    return record.inventory_set.filter(created__gte=today).order_by('created')

def get_day_before_inventories(record):
    return record.inventory_set.filter(created__gte=yesterday, created__lte=today).order_by('created')

def get_hour_interval( record, start):
    data = dict()
    inventories = get_today_inventories(record)
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

def get_hour_6(record):
    return get_hour_interval(record, 0)

def get_hour_12(record):
    interval_6 = get_hour_6(record)
    interval_12 = get_hour_interval(record, 6)
    if not isinstance(interval_6, int) and not isinstance(interval_12, int):
        return 'NaN'
    if not isinstance(interval_6, int):
        interval_6 = 0
    if not isinstance(interval_12, int):
        interval_12 = 0
    return interval_6 + interval_12

def get_hour_18(record):
    interval_12 = get_hour_12(record)
    interval_18 = get_hour_interval(record, 12)
    if not isinstance(interval_12, int) and not isinstance(interval_18, int):
        return 'NaN'
    if not isinstance(interval_12, int):
        interval_12 = 0
    if not isinstance(interval_18, int):
        interval_18 = 0
    return interval_12 + interval_18

def get_hour_24(record):
    interval_18 = get_hour_18(record)
    interval_24 = get_hour_interval(record, 18)
    if not isinstance(interval_18, int) and not isinstance(interval_24, int):
        return 'NaN'
    if not isinstance(interval_18, int):
        interval_18 = 0
    if not isinstance(interval_24, int):
        interval_24 = 0
    return interval_18 + interval_24

def get_day_before_hour_interval( record, start):
    data = dict()
    inventories = get_day_before_inventories(record)
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

def get_day_before_hour_6(record):
    return get_day_before_hour_interval(record, 0)

def get_day_before_hour_12(record):
    interval_6 = get_day_before_hour_6(record)
    interval_12 = get_day_before_hour_interval(record, 6)
    if not isinstance(interval_6, int) and not isinstance(interval_12, int):
        return 'NaN'
    if not isinstance(interval_6, int):
        interval_6 = 0
    if not isinstance(interval_12, int):
        interval_12 = 0
    return interval_6 + interval_12

def get_day_before_hour_18(record):
    interval_12 = get_day_before_hour_12(record)
    interval_18 = get_day_before_hour_interval(record, 12)
    if not isinstance(interval_12, int) and not isinstance(interval_18, int):
        return 'NaN'
    if not isinstance(interval_12, int):
        interval_12 = 0
    if not isinstance(interval_18, int):
        interval_18 = 0
    return interval_12 + interval_18

def get_day_before_hour_24(record):
    interval_18 = get_day_before_hour_18(record)
    interval_24 = get_day_before_hour_interval(record, 18)
    if not isinstance(interval_18, int) and not isinstance(interval_24, int):
        return 'NaN'
    if not isinstance(interval_18, int):
        interval_18 = 0
    if not isinstance(interval_24, int):
        interval_24 = 0
    return interval_18 + interval_24

# def render_pub(record):
#     return f'{record.link.pub}'

def render_last_refreshed(record):
    inventory = record.inventory_set.all().last()
    return inventory.created.strftime('%m/%d/%Y %H:%M')

def render_hour_6(record):
    return get_hour_6(record)

def render_hour_6_comparison(record):
    today = get_hour_6(record)
    before = get_day_before_hour_6(record)

    if isinstance(today, int) and isinstance(before, int):
        try:
            return f'{round((today - before) / before * 100, 2)}%'
        except:
            return f'{(today - before) / 1 * 100}%'
    return 'NaN'

def render_hour_12(record):
    return get_hour_12(record)

def render_hour_12_comparison(record):
    today = get_hour_12(record)
    before = get_day_before_hour_12(record)

    if isinstance(today, int) and isinstance(before, int):
        try:
            return f'{round((today - before) / before * 100, 2)}%'
        except:
            # return f'{(today - before) / 1 *100}%'
            return "0%"
    return 'NaN'

def render_hour_18(record):
    return get_hour_18(record)

def render_hour_18_comparison(record):
    today = get_hour_18(record)
    before = get_day_before_hour_18(record)

    if isinstance(today, int) and isinstance(before, int):
        try:
            return f'{round((today - before) / before * 100, 2)}%'
        except:
            # return f'{(today - before) / 1 *100}%'
            return "0%"
    return 'NaN'

def render_hour_24(record):
    return get_hour_24(record)

def render_hour_24_comparison(record):
    today = get_hour_24(record)
    before = get_day_before_hour_24(record)

    if isinstance(today, int) and isinstance(before, int):
        try:
            return f'{round((today - before) / before * 100, 2)}%'
        except:
            # return f'{(today - before) / 1 *100}%'
            return "0%"
    return 'NaN'
