from __future__ import absolute_import, unicode_literals
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

@shared_task(bind=True)
def task_get_inventory(self, pk):
    link = Link.objects.get(pk=pk)
    products = parse_product(link.link)
    for product in products:
        qs = Product.objects.filter(identity=product['identity'])
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
        link.state = dict(PROGRESS_TYPE)['done']
        link.save()


@shared_task(bind=True)
def task_get_inventory_from_type(self, pk):
    record = TypeLinkRecord.objects.get(pk=pk)
    cnt = record.link_set.count()
    
    for link in record.link_set.all():
        link.state = dict(PROGRESS_TYPE)['progress']
        link.save()
        current_app.send_task(
            'links.tasks.task_get_inventory',
            args=(link.pk, ),
            queue='inventory',
        )
    notify.send(
        sender=record,
        recipient=user,
        verb=f'</b>{cnt}</b> Links are added and scraped',
        description=f'</b>{cnt}</b> Links are added and scraped',
    )


@shared_task(bind=True)
def task_start_get_inventory(self):
    todos = Link.objects.filter(state=dict(PROGRESS_TYPE)['progress'])
    record = SchedulerLookUp.objects.create(name='Get inventories from link')
    notify.send(
        sender=record,
        recipient=user,
        verb=f'Getting inventories from link',
        description=f'Getting inventories from link',
    )
    if todos.exists():
        return False

    links = Link.objects.all()
    links.update(state=dict(PROGRESS_TYPE)['progress'])

    for link in links:
        current_app.send_task(
            'links.tasks.task_get_inventory',
            args=(link.pk, ),
            queue='inventory',
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

    Link.objects.all().exclude(link__in=unis).delete()
    ctn = 0
    for link in links:
        try:
            link = Link(**link, link_type='fetch', record=record)
            link.save()
            ctn += 1
        except IntegrityError:
            continue

    notify.send(
        sender=record,
        recipient=user,
        verb=f'</b>{ctn}</b> Links are added from Firebase DB',
        description=f'</b>{ctn}</b> Links are added from Firebase DB',
    )


# @shared_task(bind=True)
# def task_test_scheduler(self):
#     pass
    

# @shared_task(bind=True)
# def task_checker(self):
#     pass
