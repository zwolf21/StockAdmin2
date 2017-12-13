from django import forms
from django.forms import inlineformset_factory

from .models import Buy, BuyItem


BuyItemFormSet = inlineformset_factory(Buy, BuyItem,
    fields = ['buyinfo', 'amount', 'comment'],
    extra = 1,
    widgets = {
        'buyinfo': forms.widgets.HiddenInput()
    }
)