from django.shortcuts import render
from django.views.generic import *

from .models import Market, Product, BuyInfo


class ProductListView(ListView):
    model = Product
    
