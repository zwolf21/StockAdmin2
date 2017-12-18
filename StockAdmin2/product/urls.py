from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('update/<int:pk>/buyinfo/', ProductUpdateBuyInfoCreateView.as_view(), name='update-buyinfo-create'),
    path('update/api/<int:pk>/', api_update, name='api-update'),
]