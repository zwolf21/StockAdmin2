from django import forms
from .settings import START_DATE_INI, END_DATE_INI


class DateFilterForm(forms.Form):
    start_date = forms.DateField(initial=START_DATE_INI)
    end_date = forms.DateField(initial=END_DATE_INI)


class SearchFilterForm(forms.Form):
    search = forms.CharField(label='검색어', required=False)


class MixedFililter(DateFilterForm):
    search = forms.CharField(label='검색어', required=False)


