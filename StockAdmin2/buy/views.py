from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import *

from .models import Buy, BuyItem, StockRecord
from .forms import BuyForm, BuyItemInlineFormSet, BuyItemCartFormSet, BuyDateForm
from .services import buyitem_formset_operation, rollback_to_cart
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
    fields = 'commiter',

    def get_context_data(self, **kwargs):
        context = super(BuyDetailView, self).get_context_data(**kwargs)
        context['form'] = BuyForm()
        return context


class BuyUpdateView(UpdateView):
    model = Buy
    fields = 'date', 'commiter',
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
            if rollback_to_cart(formset):
                return HttpResponseRedirect(reverse('buy:buy-cart'))
        return super(BuyUpdateView, self).form_valid(form)


class BuyConfirmView(UpdateView):
    model = Buy
    fields = 'commiter',


class BuyDeleteView(DeleteView):
    model = Buy
    success_url = reverse_lazy('buy:buy-list')


class BuyItemCartFormView(FormView):
    form_class = BuyDateForm
    template_name = 'buy/buyitem_cart.html'
    success_url = reverse_lazy('buy:buy-cart')

    def get_context_data(self, **kwargs):
        context = super(BuyItemCartFormView, self).get_context_data(**kwargs)
        qs = BuyItem.objects.filter(buy__isnull=True)
        context['formset'] = BuyItemCartFormSet(self.request.POST or None, queryset=qs)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.save()
            buyitem_formset_operation(formset, form.cleaned_data['date'])
        return super(BuyItemCartFormView, self).form_valid(form)


