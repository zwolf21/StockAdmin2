from django.db.models import Q

from .smart_filter import filter_searches
from .forms import DateFilterForm, SearchFilterForm
from .settings import LOOKUP_CONTEXTS



class QueryFilter(object):
    form_classes = {
        'date': DateFilterForm,
        'search': SearchFilterForm
    }
    date_form_name = 'date_filter_form'
    search_form_name = 'search_filter_form'

    def __init__(self, request, queryset=None, app_name=None):
        self.request = request
        self.queryset = queryset
        self.app_name = app_name

    def set_filter_form_to_context(self, context, date_form_name=None, search_form_name=None):
        context[date_form_name or self.date_form_name] = self.get_date_filter_form()
        context[search_form_name or self.search_form_name] = self.get_search_filter_form()
        return self

    def get_date_filter_form(self):
        Form = self.form_classes['date']
        return Form(self.request.GET or None)

    def get_search_filter_form(self):
        Form = self.form_classes['search']
        search_form = Form(self.request.GET or None)

        # if search_form.is_valid():
        #     search = search_form.cleaned_data.get('search')
            # self.request.session['search'] = search
        # else:
            # session_search = self.request.session.get('search')
            # if session_search:
            #     search_form.fields['search'].initial = session_search
        return search_form

    def filter_by_date(self, date_field=None, queryset=None, inplace=True):
        date_form = self.get_date_filter_form()
        qs = queryset or self.queryset
        if date_field is None:
            lookup = LOOKUP_CONTEXTS.get(self.app_name)
            if lookup:
                date_fields = lookup.get('date_range')
                if date_fields:
                    date_field = date_fields[0]

        if not qs or not date_field:
            return qs

        if date_form.is_valid():
            start_date = date_form.cleaned_data.get('start_date')
            end_date = date_form.cleaned_data.get('end_date')
        else:
            start_date = date_form.fields['start_date'].initial
            end_date = date_form.fields['end_date'].initial

        date_q = Q(**{'{}__range'.format(date_field): [start_date, end_date]})
        ret = qs.filter(date_q)
        if inplace:
            self.queryset = ret
        return ret

    def filter_by_search(self, app_name=None, queryset=None, inplace=True):
        search_form = self.get_search_filter_form()
        qs = queryset or self.queryset

        if not qs:
            return qs

        if search_form.is_valid():
            searches = search_form.cleaned_data.get('search')
            qs = filter_searches(qs, searches, app_name or self.app_name)

        if inplace:
            self.queryset = qs
        return qs

    def filter_by_all(self, **kwargs):
        self.filter_by_date(inplace=True, **kwargs)
        self.filter_by_search(inplace=True, **kwargs)
        return self.queryset





