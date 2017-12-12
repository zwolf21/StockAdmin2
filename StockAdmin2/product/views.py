from django.shortcuts import render
from django.views.generic import *

from .models import Market, Product, BuyInfo
from core.filter import QueryFilter


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        qf = QueryFilter(self.request, qs)
        qs = qf.filter_by_search()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        qf = QueryFilter(self.request)
        context['search_filter_form'] = qf.get_search_filter_form()
        return context
    

class ProductDetailView(DetailView):
    model = Product
