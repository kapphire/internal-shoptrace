from django.conf import settings
from django.db import models

class Link(models.Model):
    INSERT = 'insert'
    FETCH = 'fetch'

    LINK_TYPE = (
        (INSERT, INSERT),
        (FETCH, FETCH),
    )

    link = models.CharField(max_length=2000, unique=True)
    key = models.CharField(blank=True, null=True, max_length=50)
    sub_key = models.CharField(blank=True, null=True, max_length=50)
    pub = models.CharField(blank=True, null=True, max_length=50)
    link_type = models.CharField(max_length=20, choices=LINK_TYPE)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10, blank=True, null=True)

    record = models.ForeignKey('links.SchedulerRecord', on_delete=models.CASCADE, blank=True, null=True)
    insert = models.ForeignKey('links.TypeLinkRecord', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.link


class Product(models.Model):
    identity = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    link = models.ForeignKey('links.Link', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    qty = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey('links.Product', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.qty)


class SchedulerLookUp(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SchedulerRecord(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class TypeLinkRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created.strftime('%m/%d/%Y')
