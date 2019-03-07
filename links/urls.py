from django.urls import path
from links import views

urlpatterns = [
    path('type/', views.TypeLinkListView.as_view(), name='type-link-list'),
    path('type/<int:pk>/', views.ProductListView.as_view(), name='type-link-product-list'),
    path('product/<int:pk>/', views.InventoryListView.as_view(), name='type-link-inventory-list'),
    path('period/', views.PeriodLinkListView.as_view(), name='period-link-list'),
    path('period/<int:pk>/', views.ProductListView.as_view(), name='period-link-product-list'),
    path('insert/', views.LinkInsertView.as_view(), name='type-link-add'),
    path('fetch/', views.GetPeriodLinkView.as_view(), name='period-link-add'),
]