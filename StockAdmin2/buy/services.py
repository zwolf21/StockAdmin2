from django.db.models import Count

from .models import Buy, BuyItem


def _get_selected_queryset_from_formset(formset):
    queryset = formset.get_queryset()
    selected_formset = filter(lambda form:form.cleaned_data.get('selected'), formset)
    id_list = [form.instance.id for form in selected_formset]
    return queryset.filter(id__in=id_list)


def _generate_buy_groupby_by_market(queryset, buy_date):
    market_set = queryset.order_by('buyinfo__market').values('buyinfo__market').annotate(
        market_count=Count('buyinfo__market', distinct=True)
    )
    for market_dict in market_set:
        market = market_dict['buyinfo__market']
        new_buy = Buy.objects.create(date=buy_date)
        queryset.filter(buyinfo__market=market).update(buy=new_buy)


def rollback_to_cart(formset):
    queryset = _get_selected_queryset_from_formset(formset)
    cart_set = BuyItem.objects.filter(buy__isnull=True)
    cart_exist_buyinfo_set = cart_set.values_list('buyinfo', flat=True)
    rollback_set =  queryset.exclude(buyinfo__in=cart_exist_buyinfo_set)
    cart_exist_set = queryset.filter(buyinfo__in=cart_exist_buyinfo_set)
    if rollback_set.exists():
        rollback_set.update(buy=None)
        if not cart_exist_set.exists():
            return True
    return False


def buyitem_formset_operation(formset, buy_date):
    selected_set = _get_selected_queryset_from_formset(formset)
    _generate_buy_groupby_by_market(selected_set, buy_date)


def stockrecord_formset_operation(formset, stock_date=None):
    for stockrecord_form in formset:
        if stockrecord_form.is_valid():
            buyitem = stockrecord_form.instance.buyitem
            if stockrecord_form.cleaned_data['amount'] > 0 and stock_date:
                stockrecord_form.instance.date = stock_date
            elif stockrecord_form.cleaned_data['end'] == True:
                buyitem.isend = True
                buyitem.save()                
            stockrecord_form.save()



