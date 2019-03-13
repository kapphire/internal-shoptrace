from __future__ import absolute_import, unicode_literals
import pyrebase
from dateutil.parser import parse
from celery import current_app, shared_task
from celery.result import AsyncResult
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError

from links.models import (
    Link,
    Product,
    Inventory,
    SchedulerTestRecord
)
from links.handler import parse_product

PROGRESS_TYPE = (
    ('progress', 'progress'),
    ('done', 'done'),
)
ctn = 0

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
def task_get_inventory_from_type(self, ids):
    for pk in ids:
        link = Link.objects.get(pk=pk)
        link.state = dict(PROGRESS_TYPE)['progress']
        link.save()
        current_app.send_task(
            'links.tasks.task_get_inventory',
            args=(link.pk, ),
            queue='inventory',
        )
        # task_get_inventory(link)


@shared_task(bind=True)
def task_start_get_inventory(self):
    obj = SchedulerTestRecord.objects.last()
    if not obj:
        SchedulerTestRecord.objects.create(number=1, name='task_start_get_inventory')
    else:
        number = obj.number + 1
        SchedulerTestRecord.objects.create(number=number, name='task_start_get_inventory')

    todos = Link.objects.filter(state=dict(PROGRESS_TYPE)['progress'])
    
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
        # task_get_inventory(link)


@shared_task(bind=True)
def task_fetch_link_from_firebase(self):
    obj = SchedulerTestRecord.objects.last()
    if not obj:
        SchedulerTestRecord.objects.create(number=1, name='task_fetch_link_from_firebase')
    else:
        number = obj.number + 1
        SchedulerTestRecord.objects.create(number=number, name='task_fetch_link_from_firebase')

    links = list()
    unis = list()
    firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
    db = firebase.database()
    products = db.child("products").get().val()

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

    for link in links:
        try:
            link = Link(**link, link_type='fetch')
            link.save()
        except IntegrityError:
            continue


# @shared_task(bind=True)
# def task_test_scheduler(self):
#     for i in range(0, 9):
#         current_app.send_task(
#             'links.tasks.task_checker',
#             queue='inventory',
#         )
    

# @shared_task(bind=True)
# def task_checker(self):
#     pass
