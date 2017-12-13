from django import forms
from django.forms import inlineformset_factory

from .models import Buy, BuyItem


class BuyItemForm(forms.ModelForm):
    selected = forms.BooleanField(initial=False, required=False)
    buyinfo_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': '검색어 입력'}))
    class Meta:
        model = BuyItem
        fields = 'buy', 'buyinfo', 'amount', 'comment',
        widgets = {
            'buyinfo': forms.widgets.HiddenInput()
        }

    # def __init__(self, *args, **kwargs):
    #     super(BuyItemForm, self).__init__(*args, **kwargs)
    #     BuyInfo = self.fields['buyinfo'].queryset.model
    #     self.fields['buyinfo'].queryset = BuyInfo.objects.filter(active=True)


BuyItemInlineFormSet = inlineformset_factory(Buy, BuyItem, BuyItemForm,
    extra=1,
    can_delete=True,
    can_order=True,
)