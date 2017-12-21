from django.urls import path

from .views import *

app_name = 'autocomplete'
urlpatterns = [
    path('api/buyinfo/', BuyInfoListAPIView.as_view(), name='api-buyinfo'),
    path('api/buyinfo/<slug:slug>/', BuyInfoListAPIView.as_view(), name='api-buyinfo-market'),
]