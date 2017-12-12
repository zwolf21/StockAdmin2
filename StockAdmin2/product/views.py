from django.shortcuts import render
from django.views.generic import *

from .models import Market, Product, BuyInfo
from .forms import get_buyinfo_inline_formset
from core.filter import QueryFilter


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        qf = QueryFilter(self.request, qs)
        return qf.filter_by_search()
        
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        qf = QueryFilter(self.request)
        context['search_filter_form'] = qf.get_search_filter_form()
        return context
    

class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'code', 'name', 'company', 'std_unit', 'pkg_amount', 'etc_class',
    formset_extra = 0

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['formset']=get_buyinfo_inline_formset(
            self.request, self.get_object(), extra=self.formset_extra
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset.save()
        return super(ProductUpdateView, self).form_valid(form)

class ProductUpdateBuyInfoCreateView(ProductUpdateView):
    formset_extra = 1

