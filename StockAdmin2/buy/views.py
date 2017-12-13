from django.shortcuts import render
from django.views.generic import *

from .models import Buy, BuyItem, StockRecord
from .forms import BuyItemInlineFormSet, BuyItemCartFormSet, BuyDateForm

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


class BuyListView(ListView):
    model = Buy


class BuyDetailView(DetailView):
    model = Buy


class BuyUpdateView(UpdateView):
    model = Buy
    fields = 'date',
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(BuyUpdateView, self).get_context_data(**kwargs)
        formset = BuyItemInlineFormSet(self.request.POST or None, instance=self.get_object())
        context['formset'] = formset
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.save()
        return super(BuyUpdateView, self).form_valid(form)


class BuyItemCartFormView(FormView):
    form_class = BuyDateForm
    template_name = 'buy/buyitem_cart.html'
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(BuyItemCartFormView, self).get_context_data(**kwargs)
        qs = BuyItem.objects.filter(buy__isnull=True)
        context['formset'] = BuyItemCartFormSet(self.request.POST or None, queryset=qs)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.save()
        return super(BuyItemCartFormView, self).form_valid(form)






