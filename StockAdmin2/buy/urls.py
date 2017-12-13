from django.urls import path

from .views import *


app_name = 'buy'
urlpatterns = [
    # path('test/', TestView.as_view(), name='test'),
    path('', BuyListView.as_view(), name='buy-list'),
    path('cart/', BuyItemCartFormView.as_view(), name='buy-cart'),
    path('<slug:slug>/', BuyDetailView.as_view(), name='buy-detail'),
    path('update/<slug:slug>/', BuyUpdateView.as_view(), name='buy-update'),
]