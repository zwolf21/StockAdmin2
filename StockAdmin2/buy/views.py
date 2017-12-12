from django.shortcuts import render
from django.views.generic import *

from .models import Buy, BuyItem, StockRecord

from core.filter import QueryFilter

class TestView(ListView):
    model = BuyItem
    template_name = 'buy/test.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        qf = QueryFilter(self.request)
        context['date_filter_form'] = qf.get_date_filter_form()
        context['search_filter_form'] = qf.get_search_filter_form()
        return context

    def get_queryset(self):
        qs = super(TestView, self).get_queryset()
        qf = QueryFilter(self.request, qs)
        qs = qf.filter_by_date('buy__date')
        qs = qf.filter_by_search(queryset=qs)
        return qs

