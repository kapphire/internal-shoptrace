from django.urls import path
from links import views

urlpatterns = [
    path('', views.AllLinkListView.as_view(), name='all-link-list'),
    path('type/', views.TypeLinkListView.as_view(), name='type-link-list'),
    path('type-history/', views.TypeLinkHistoryListView.as_view(), name='type-link-history-list'),
    path('type-history/<int:pk>/', views.TypeLinkHistoryDetailView.as_view(), name='type-link-history-detail'),
    path('type/<int:pk>/', views.ProductListView.as_view(), name='type-link-product-list'),
    path('product/<int:pk>/', views.InventoryListView.as_view(), name='type-link-inventory-list'),
    path('period/', views.PeriodLinkListView.as_view(), name='period-link-list'),
    path('period/<int:pk>/', views.ProductListView.as_view(), name='period-link-product-list'),
    path('insert/', views.LinkInsertView.as_view(), name='type-link-add'),
    path('fetch/', views.GetPeriodLinkView.as_view(), name='period-link-add'),
    path('scheduler-record/', views.SchedulerRecordListView.as_view(), name='scheduler-record-list'),
    path('scheduler-record/<int:pk>/', views.SchedulerRecordDetailView.as_view(), name='scheduler-record-detail'),
    path('scraper-record/', views.ScraperRecordListView.as_view(), name='scraper-record-list'),
    path('moving-product/', views.MovingProductListView.as_view(), name='moving-product-list'),
    path('commafeed/', views.CommaFeedListView.as_view(), name='commafeed-list'),
    
    path('product/', views.ProductInventory)
]