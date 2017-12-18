from django.urls import path

from .views import *


app_name = 'buy'
urlpatterns = [
    path('', BuyListView.as_view(), name='buy-list'),
    path('cart/', BuyItemCartFormView.as_view(), name='buy-cart'),
    path('<slug:slug>/', BuyDetailView.as_view(), name='buy-detail'),
    path('update/<slug:slug>/', BuyUpdateView.as_view(), name='buy-update'),
    path('delete/<slug:slug>/', BuyDeleteView.as_view(), name='buy-delete'),
    path('confirm/<slug:slug>/', BuyConfirmView.as_view(), name='buy-confirm'),

    path('stockrecord/stocking/', StockRecordStockingView.as_view(), name='stock-stocking'),
    path('stockrecord/stocked/', stockrecord_stocked_view, name='stock-stocked'),
    path('stockrecord/agg/<slug:type>/', StockRecordAggregateView.as_view(), name='stock-agg'),
    path('buyitem/agg/<slug:type>/', BuyItemAggregateView.as_view(), name='buy-agg'),
    path('buyitem/update-set/', buyitem_update_view, name='buyitem-update-set'),
]