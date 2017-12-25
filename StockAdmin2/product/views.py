from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import *

from djangoslicer import SlicePaginatorMixin

from .models import Market, Product, BuyInfo
from .forms import get_buyinfo_inline_formset
from core.filter import QueryFilter
from core.restapi.updater import smart_update



class ProductListView(SlicePaginatorMixin, ListView):
    model = Product
    paginate_by = 25

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
    fields = [
                'code', 'name', 'company', 'std_unit', 'pkg_amount', 'etc_class', 
                'apply_root', 'unit', 'unit_amount', 'op_type', 'edi_code',
            ]
    formset_extra = 0
    success_url = '.'

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


def api_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    smart_update(product)
    return redirect(reverse('product:update', args=(pk,)))








