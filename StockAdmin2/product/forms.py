from django import forms
from django.forms import inlineformset_factory

from .models import Market, Product, BuyInfo


def get_buyinfo_inline_formset(request, instance, **kwargs):
    fields = [
        'product', 'market', 'date', 'price', 'active',
        'pro_type', 'pay_type', 'buy_edi_code'
    ]
    FormSet = inlineformset_factory(Product, BuyInfo, fields=fields, can_delete=True, **kwargs)
    if request.method == "POST":
        return FormSet(request.POST or None, instance=instance)
    return FormSet(instance=instance)

