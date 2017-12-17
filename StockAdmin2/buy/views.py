from pprint import pprint

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import *

from .models import Buy, BuyItem, StockRecord
from .forms import BuyForm, BuyItemInlineFormSet, BuyItemCartFormSet, DateForm, StockRecordFormSet
from .services import buyitem_formset_operation, rollback_to_cart, stockrecord_formset_operation
from core.filter import QueryFilter



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
    form_class = DateForm
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


from core.dfapi import QuerySetDataFrame, df_to_records

class BuyItemAggregateView(ListView):
    model = BuyItem
    template_name = 'buy/buyitem_agg.html'

    def get_context_data(self, **kwargs):
        context = super(BuyItemAggregateView, self).get_context_data(**kwargs)
        agg_type = self.kwargs.get('type')
        qs = self.get_queryset().filter(buy__isnull=False, buy__commiter__isnull=False)
        qf = QueryFilter(self.request, queryset=qs)
        qf.set_filter_form_to_context(context)
        buyitem_set = qf.filter_by_all()
        stockrecord_set = StockRecord.objects.filter(buyitem__in=buyitem_set, amount__gt=0)
        bqsd = QuerySetDataFrame(buyitem_set)
        sqsd = QuerySetDataFrame(stockrecord_set)
        buyitem_df = bqsd.annotate(agg_type)
        stockrecord_df = sqsd.annotate(agg_type)
        merge_on = 'id_{}'.format(agg_type.lower())
        df = stockrecord_df[[merge_on, 'stocked_amount_sum', 'stocked_price_sum']].merge(buyitem_df, on=merge_on)
        df['is_completed'] = (df.stocked_amount_sum == df.buy_amount_sum)
        df.loc[df.is_completed == False, ['is_completed']] = df['isend'] 
        context['object_list'] = df_to_records(df)
        return context



class StockRecordAggregateView(ListView):
    model = StockRecord
    template_name = 'buy/stocked_agg.html'

    def get_context_data(self, **kwargs):
        context = super(StockRecordAggregateView, self).get_context_data(**kwargs)
        agg_type = self.kwargs.get('type')
        qs = self.get_queryset()
        qf = QueryFilter(self.request, queryset=qs, app_name='StockRecord-stocked')
        qf.set_filter_form_to_context(context)
        # print(qs)
        qs = qf.filter_by_all()
        annoset, total_stocked_price = qs.group_by_fk(agg_type)
        context['object_list'] = annoset
        context['total_stocked_price'] = total_stocked_price
        return context



class StockRecordStockingView(FormView):
    form_class = DateForm
    success_url = '.'
    template_name = 'buy/stocking_form.html'

    def get_context_data(self, **kwargs):
        context = super(StockRecordStockingView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = StockRecordFormSet(self.request.POST or None)
        else:
            qs = StockRecord.objects.filter(
                buyitem__buy__commiter__isnull=False,
                amount=0,
                buyitem__isend=False
            )
            qf = QueryFilter(self.request, app_name='StockRecord-stocking', queryset=qs)
            qf.set_filter_form_to_context(context)
            qs = qf.filter_by_all()
            context['formset'] = StockRecordFormSet(queryset=qs)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        stock_date = form.cleaned_data['date']
        stockrecord_formset_operation(formset, stock_date)
        return super(StockRecordStockingView, self).form_valid(form)



def stockrecord_stocked_view(request):
    context = {}
    if request.method == "POST":
        formset = StockRecordFormSet(request.POST or None)
        stockrecord_formset_operation(formset)
        if formset.is_valid(): # 뒤에 호출하여야 DELETE가 먹힘
            formset.save()
        return redirect('.')
    else:
        qs = StockRecord.objects.filter(amount__gt=0)
        qf = QueryFilter(request, queryset=qs, app_name='StockRecord-stocked')
        qf.set_filter_form_to_context(context)
        qs = qf.filter_by_all()
        context['formset'] = StockRecordFormSet(queryset=qs)
        return render(request, 'buy/stocked_form.html', context)














