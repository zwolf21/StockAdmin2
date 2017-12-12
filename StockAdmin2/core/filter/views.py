from django.db.models import Q

from .smart_filter import filter_searches
from .forms import DateFilterForm, SearchFilterForm



class QueryFilter(object):
    form_classes = {
        'date': DateFilterForm,
        'search': SearchFilterForm
    }

    def __init__(self, request, queryset=None):
        self.request = request
        self.queryset = queryset


    def get_date_filter_form(self):
        Form = self.form_classes['date']
        return Form(self.request.GET or None)


    def get_search_filter_form(self):
        Form = self.form_classes['search']
        search_form = Form(self.request.GET or None)

        if search_form.is_valid():
            search = search_form.cleaned_data.get('search')
            self.request.session['search'] = search
        else:
            session_search = self.request.session.get('search')
            if session_search:
                search_form.fields['search'].initial = session_search
        return search_form


    def filter_by_date(self, date_field, queryset=None):
        date_form = self.get_date_filter_form()
        qs = queryset or self.queryset

        if not qs:
            return qs

        if date_form.is_valid():
            start_date = date_form.cleaned_data.get('start_date')
            end_date = date_form.cleaned_data.get('end_date')
        else:
            start_date = date_form.fields['start_date'].initial
            end_date = date_form.fields['end_date'].initial

        date_q = Q(**{'{}__range'.format(date_field): [start_date, end_date]})
        return qs.filter(date_q)


    def filter_by_search(self, app_name=None, queryset=None):
        search_form = self.get_search_filter_form()
        qs = queryset or self.queryset

        if not qs:
            return qs

        if search_form.is_valid():
            searches = search_form.cleaned_data.get('search')
            return filter_searches(qs, searches, app_name)

        return qs





