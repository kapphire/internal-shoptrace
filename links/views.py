from celery import current_app
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django_tables2 import SingleTableView

from .forms import LinkInsertForm, GetPeriodLinkForm
from .models import Link, Product, Link, Inventory
from .tables import (
    LinkTable,
    ProductTable,
    InventoryTable,
)

class TypeLinkListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = LinkTable

    def get_queryset(self):
        return Link.objects.filter(link_type='insert')


class PeriodLinkListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = LinkTable

    def get_queryset(self):
        return Link.objects.filter(link_type='fetch')


class ProductListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = ProductTable

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        link = get_object_or_404(Link, pk=pk)
        if not link.product_set.all():
            return Product.objects.none()
        return link.product_set.all()


class InventoryListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = InventoryTable

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        if not product.inventory_set.all():
            return Inventory.objects.none()
        return product.inventory_set.all()


class LinkInsertView(FormView):
    template_name = 'links/link_insert.html'
    form_class = LinkInsertForm
    success_url = reverse_lazy('links:type-link-list')

    def form_valid(self, form):
        links = form.cleaned_data['links'].splitlines()
        ids = list()
        for link in links:
            try:
                link = Link(link=link, link_type='insert')
                link.save()
                ids.append(link.pk)
            except IntegrityError:
                continue
        current_app.send_task(
            'links.tasks.task_get_inventory_from_type',
            args=(ids,),
            queue='inventory',
        )
        return super().form_valid(form)


class GetPeriodLinkView(FormView):
    template_name = 'links/get_period_link.html'
    form_class = GetPeriodLinkForm
    success_url = reverse_lazy('links:period-link-list')

    def form_valid(self, form):
        current_app.send_task(
            'links.tasks.task_fetch_link_from_firebase',
            queue='inventory',
        )
        return super().form_valid(form)
