from __future__ import absolute_import, unicode_literals
import time
import json
import requests
import xmltodict
import pyrebase
from dateutil.parser import parse
from celery import current_app, shared_task
from celery.result import AsyncResult
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from notifications.signals import notify

User = get_user_model()
user = User.objects.first()

from links.models import (
    Link,
    Product,
    Inventory,
    SchedulerRecord,
    SchedulerLookUp,
    TypeLinkRecord,
)
from links.handler import parse_product

PROGRESS_TYPE = (
    ('progress', 'progress'),
    ('done', 'done'),
)

MODEL_MAPPING = {
    'TypeLinkRecord': TypeLinkRecord,
    'SchedulerRecord': SchedulerRecord,
    'SchedulerLookUp': SchedulerLookUp
}

@shared_task(bind=True)
def task_get_inventory(self, pk, record_pk, model):
    link = Link.objects.get(pk=pk)
    record = MODEL_MAPPING[model].objects.get(pk=record_pk)
    products = parse_product(link.link)
    for product in products:
        qs = link.product_set.all().filter(identity=product['identity'])
        if not qs.exists():
            obj = Product.objects.create(
                name=product['name'],
                vendor=product['vendor'],
                identity=product['identity'],
                link=link,
            )
        else:
            obj = qs.first()
        inventory = Inventory.objects.create(qty=product['quantity'], product=obj)
        if model == 'SchedulerRecord':
            record.links.add(link)
    link.state = dict(PROGRESS_TYPE)['done']            
    link.save()


@shared_task(bind=True)
def task_get_inventory_from_type(self, pk):
    record = TypeLinkRecord.objects.get(pk=pk)
    model = record._meta.model.__name__
    
    reg = 0
    for link in record.link_set.all():
        reg += 1
        if not reg % 4:
            time.sleep(15)
        link.state = dict(PROGRESS_TYPE)['progress']
        link.save()
        current_app.send_task(
            'links.tasks.task_get_inventory',
            args=(link.pk, record.pk, model),
            queue='inventory',
        )

    cnt = record.link_set.count()
    notify.send(
        sender=record,
        recipient=user,
        verb=f'</b>{cnt}</b> Links are added and scraped',
        description=f'</b>{cnt}</b> Links are added and scraped',
    )


@shared_task(bind=True)
def task_start_get_inventory(self):
    todos = Link.objects.filter(state=dict(PROGRESS_TYPE)['progress'])
    record = SchedulerRecord.objects.create(name='Get inventories from link')
    model = record._meta.model.__name__
    
    if todos.exists():
        notify.send(
            sender=record,
            recipient=user,
            verb=f'Start getting inventory task skipped',
            description=f'Start getting inventory task skipped.',
        )
        return False

    links = Link.objects.exclude(link_type='commafeed')
    links.update(state=dict(PROGRESS_TYPE)['progress'])
    reg = 0
    for link in links:
        reg += 1
        if not reg % 4:
            time.sleep(10)
        current_app.send_task(
            'links.tasks.task_get_inventory',
            args=(link.pk, record.pk, model),
            queue='inventory',
        )
    cnt = links.count()
    notify.send(
        sender=record,
        recipient=user,
        verb=f'</b>{cnt}</b> Links are scraped',
        description=f'</b>{cnt}</b> Links are scraped',
    )


@shared_task(bind=True)
def task_fetch_link_from_firebase(self):
    links = list()
    unis = list()
    firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
    db = firebase.database()
    products = db.child("products").get().val()

    record = SchedulerRecord.objects.create(name='Fetch link from Firebase')

    for key, product in products.items():
        for sub_key, item in product.items():
            valid = dict()
            pub = item.get('pub')
            try:
                pub_obj = parse(pub).replace(tzinfo=None)
                timedelta = timezone.now().replace(tzinfo=None) - pub_obj
                if timedelta.days > settings.PERIOD:
                    continue
                valid['key'] = key
                valid['sub_key'] = sub_key
                valid['link'] = item.get('link')
                valid['pub'] = item.get('pub')
                links.append(valid)
                unis.append(item.get('link'))
            except ValueError:
                continue

    Link.objects.filter(link_type='fetch').exclude(link__in=unis).update(deprecated=True)
    ctn = 0
    for link in links:
        try:
            link = Link(**link, link_type='fetch')
            link.save()
            record.links.add(link)
            ctn += 1
        except IntegrityError:
            continue

    notify.send(
        sender=record,
        recipient=user,
        verb=f'</b>{ctn}</b> Links are added from Firebase DB',
        description=f'</b>{ctn}</b> Links are added from Firebase DB',
    )


@shared_task(bind=True)
def task_fetch_link_from_commafeed(self):
    Link.objects.filter(link_type='commafeed').update(deprecated=True)
    record = SchedulerRecord.objects.create(name='Fetch link from CommaFeed')

    url = 'https://www.commafeed.com/rest/category/get'
    sites = json.loads(requests.get(url, auth=("Producthunter", "hamham11")).text)['feeds']
    cnt = 0
    
    for site in sites:
        try:
            feed = site['feedUrl']
            feed_xml = xmltodict.parse(requests.get(feed).text)
            for key, value in feed_xml.items():
                entries = value['entry']
                for entry in entries:
                    cnt += 1
                    updated = parse(entry['updated']).replace(tzinfo=None)
                    timedelta = timezone.now().replace(tzinfo=None) - updated

                    if timedelta.days >= 1:
                        continue
                    try:
                        link = entry['link']['@href']
                        products = parse_product(link)
                        time.sleep(5)

                        if not products:
                            continue

                        qs_link = Link.objects.filter(link_type='commafeed').filter(link=link)
                        if not qs_link.exists():
                            cnt += 1
                            link_obj = Link.objects.create(link=link, link_type='commafeed')
                        else:
                            link_obj = qs_link.first()
                            link_obj.deprecated = False
                            link_obj.save()

                        for product in products:
                            identity = product.get('identity')
                            if not identity:
                                continue
                            qs = link_obj.product_set.all().filter(identity=product['identity'])
                            if not qs.exists():
                                prod_obj = Product.objects.create(
                                    name=product.get('name'),
                                    vendor=product.get('vendor'),
                                    identity=product.get('identity'),
                                    link=link_obj,
                                )
                            else:
                                prod_obj = qs.first()
                            try:
                                inventory = Inventory.objects.create(qty=product['quantity'], product=prod_obj)
                            except Exception as e:
                                continue
                    except Exception as e:
                        continue
        except Exception as e:
            continue
    notify.send(
        sender=record,
        recipient=user,
        verb=f'</b>{cnt}</b> Links are added from CommaFeed',
        description=f'</b>{cnt}</b> Links are added from CommaFeed',
    )
