from django.utils import timezone
from django import forms
from django.forms import inlineformset_factory, modelformset_factory, modelform_factory

from .models import Buy, BuyItem


class BuyForm(forms.ModelForm):

    class Meta:
        model = Buy
        fields = 'commiter',



class BuyItemForm(forms.ModelForm):
    selected = forms.BooleanField(initial=False, required=False)
    buyinfo_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': '검색어 입력'}))
    class Meta:
        model = BuyItem
        fields = 'buy', 'buyinfo', 'amount', 'comment',
        widgets = {
            'buyinfo': forms.widgets.HiddenInput()
        }


class BuyDateForm(forms.Form):
    date = forms.DateField(label='구매일자', initial=timezone.now(), required=False)


BuyItemInlineFormSet = inlineformset_factory(Buy, BuyItem, BuyItemForm,
    extra=1,
    can_delete=True,
    can_order=True,
)



BuyItemCartFormSet = modelformset_factory(BuyItem, BuyItemForm,
    extra = 1,
    can_delete = True,
)

