import re
from django.db.models import Q
from django.utils.timezone import now, timedelta

from .settings import *

from ..models import ETC_CLASS, Market


def is_exclude_query(keyword):
    if keyword.startswith('-') or keyword.endswith('-'):
        return True
    return False

def is_date_field(keyword):
    if keyword in DATE_FIELDS:
        return True
    return False

def get_date_range_by_keyword(search, date_keywordset=DATE_KEYWORD_SET):
    if search not in date_keywordset:
        return START_DATE_INI, END_DATE_INI
    if search in ['어제', 'ㅇㅈ']:
        date = now() - timedelta(1)
    elif search in ['오늘', 'ㅇㄴ']:
        date = now()
    elif search in ['그제', 'ㄱㅈ']:
        date = now() - timedelta(2)
    elif search in ['내일', 'ㄴㅇ']:
        date = now() + timedelta(1)
    return date, date


def get_icontains_q(field, search):
    return Q(**{'{}__icontains'.format(field): search})

def get_contains_q(field, search):
    return Q(**{'{}__contains'.format(field): search})

def get_exact_q(field, search):
    return Q(**{'{}__exact'.format(field): search})

def get_iexact_q(field, search):
    return Q(**{'{}__iexact'.format(field): search})

def get_date_keyword_q(field, search):
    date_range = get_date_range_by_keyword(search)
    return Q(**{'{}__range'.format(field): date_range})


def guess_lookup(search):
    if search in DATE_KEYWORD_SET:
        return 'date_range'
    elif search in ETC_CLASS:
        return 'etc_class'
    elif Market.objects.filter(name__contains=search).exists():
        return 'market'
    elif re.match(r'\d{8}-\d{3}', search):
        return 'slug'
    else:
        return 'contains'


def generate_search_keyword_q(model_name, keywords, filter_lookups=LOOKUP_CONTEXTS):
    context = filter_lookups.get(model_name)

    if not context:
        return Q()

    lookup_set = {}
    for search in keywords:
        lookup = guess_lookup(search)
        lookup_set.setdefault(lookup, []).append(search)

    q = ~Q()
    for lookup, searches in lookup_set.items():
        uni_q = Q()
        fields = context.get(lookup, [])
        for search in searches:
            for field in fields:
                if lookup in ['date_range']:
                    uni_q|=get_date_keyword_q(field, search)
                elif lookup in ['contains', 'market']:
                    uni_q|=get_contains_q(field, search)
                elif lookup in ['slug', 'etc_class']:
                    uni_q|=get_exact_q(field, search)
                else:
                    uni_q|=get_exact_q(field, search)
        q&=uni_q
    return q


def filter_searches(queryset, search, app_name):
    keywords = search.split()
    model_name = app_name or queryset.model.__name__

    include_keywords = filter(lambda kw: not is_exclude_query(kw),keywords)
    exclude_keywords = map(lambda kw: kw.strip('-'),
        filter(lambda kw: is_exclude_query(kw),
            keywords
        )
    )
    include_q = generate_search_keyword_q(model_name, include_keywords)
    exclude_q = generate_search_keyword_q(model_name, exclude_keywords)

    return queryset.filter(include_q).exclude(exclude_q)













