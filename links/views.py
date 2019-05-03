from celery import current_app
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.http import JsonResponse

from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView

from .forms import LinkInsertForm, GetPeriodLinkForm
from .models import (
    Link,
    Product,
    Inventory,
    SchedulerLookUp,
    SchedulerRecord,
    TypeLinkRecord,
    BestProduct,
)
from .filters import LinkFilter
from .tables import (
    LinkTable,
    ProductTable,
    SpecialProductTable,
    InventoryTable,
    ScraperRecordTable,
    SchedulerRecordTable,
    TypeLinkRecordTable,
    CommaFeedLinkTable,
    BestProductTable,
)

class AllLinkListView(SingleTableMixin, FilterView):
    template_name = 'links/list.html'
    table_class = LinkTable
    filterset_class = LinkFilter
    strict = False


class TypeLinkListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = LinkTable

    def get_queryset(self):
        return Link.objects.filter(link_type='insert').filter(deprecated=False)


class CommaFeedListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = CommaFeedLinkTable

    def get_queryset(self):
        return Link.objects.filter(link_type='commafeed').filter(deprecated=False)


class TypeLinkHistoryListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = TypeLinkRecordTable

    def get_queryset(self):
        return TypeLinkRecord.objects.all()


class TypeLinkHistoryDetailView(SingleTableView):
    template_name = 'links/list.html'
    table_class = LinkTable

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        record = get_object_or_404(TypeLinkRecord, pk=pk)
        if not record.link_set.all():
            return Link.objects.none()
        return record.link_set.all()


class PeriodLinkListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = LinkTable

    def get_queryset(self):
        return Link.objects.filter(link_type='fetch').filter(deprecated=False)


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
        return product.inventory_set.all().order_by('-created')


class SchedulerRecordListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = SchedulerRecordTable

    def get_queryset(self):
        return SchedulerRecord.objects.all()


class ScraperRecordListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = ScraperRecordTable

    def get_queryset(self):
        return SchedulerLookUp.objects.all()


class SchedulerRecordDetailView(SingleTableView):
    template_name = 'links/list.html'
    table_class = LinkTable

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        record = get_object_or_404(SchedulerRecord, pk=pk)
        if not record.links.all():
            return Link.objects.none()
        return record.links.all()


class LinkInsertView(FormView):
    template_name = 'links/link_insert.html'
    form_class = LinkInsertForm
    success_url = reverse_lazy('links:type-link-list')

    def form_valid(self, form):
        links = form.cleaned_data['links'].splitlines()
        record = TypeLinkRecord.objects.create()

        for link in links:
            try:
                link = Link(link=link, link_type='insert', insert=record)
                link.save()
            except IntegrityError:
                continue
        current_app.send_task(
            'links.tasks.task_get_inventory_from_type',
            args=(record.pk,),
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


class MovingProductListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = SpecialProductTable

    def get_queryset(self):
        targets = list()
        products = Product.objects.filter(link__deprecated=False)
        for product in products:
            qtys = set(list(product.inventory_set.values_list('qty', flat=True)))
            if len(qtys) > 1:
                targets.append(product.pk)
        products = products.filter(pk__in=targets)
        return products


class BestProductRecordListView(SingleTableView):
    template_name = 'links/list.html'
    table_class = BestProductTable

    def get_queryset(self):
        return BestProduct.objects.all()


class BestProductRecordDetailView(SingleTableView):
    template_name = 'links/list.html'
    table_class = ProductTable

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        record = get_object_or_404(BestProduct, pk=pk)
        if not record.products.all():
            return Product.objects.none()
        return record.products.all()


@csrf_exempt
def ProductInventory(request):
    response = dict()
    if request.is_ajax():
        product_id = request.POST['id']
        product = Product.objects.get(pk=product_id)        
        inventories = product.inventory_set.order_by("created").all()
        # response['quantity'] = dict()        
        # response['quantity']['pk'] = product.pk
        # response['quantity'][product.name] = list()
        # response['sale'] = dict()
        # response['sale']['pk'] = product.pk
        # response['sale'][product.name] = list()
        response['pk'] = product.pk
        response['quantity'] = dict()
        response['sale'] = dict()
        response['quantity'][product.name] = list()
        response['sale'][product.name] = list()

        qty = inventories.first().qty
        for inventory in inventories:
            # quantity element
            qty_elem = dict()
            qty_elem['Date'] = inventory.created.strftime('%Y-%m-%d %H:%M')
            qty_elem['Quantity'] = inventory.qty
            response['quantity'][product.name].append(qty_elem)
            # sale element
            # qty = inventory.qty
            if inventory.qty < qty:
                sale_elem = dict()
                sale_elem['Date'] = inventory.created.strftime('%Y-%m-%d %H:%M')
                sale_elem['Quantity'] = qty - inventory.qty
                response['sale'][product.name].append(sale_elem)
            qty = inventory.qty
    return JsonResponse(response, safe=False)
