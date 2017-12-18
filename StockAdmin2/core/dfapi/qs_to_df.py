from django_pandas.io import read_frame
from django.db.models import F

from ..models import *


def queryset_to_dataframe(queryset):
    model = queryset.model

    if model == Market:
        queryset = queryset.annotate(market=F('id'))
        df = read_frame(queryset,
            fieldnames=['market', 'name']
        )
        df.rename(
            columns={'name': 'market_name'},
            inplace=True
        )
    elif model == Product:
        queryset = queryset.annotate(product=F('id'))
        df = read_frame(queryset,
            fieldnames=[
                'product',
                'code', 'name', 'company', 'std_unit', 'pkg_amount', 'etc_class'
            ]
        )
        df.rename(
            columns={'code': 'product_code', 'name': 'product_name'},
            inplace=True
        )
    elif model == BuyInfo:
        queryset = queryset.annotate(
            buyinfo=F('id'),
            product=F('product_id'),
            market=F('market_id')
        )
        df = read_frame(queryset,
            fieldnames=[
                'buyinfo', 'market', 'product',
                'price', 'slug', 'date', 'active'
            ]
        )
        df.rename(
            columns={'slug': 'buyinfo_slug',
                'date': 'buyinfo_date', 'active': 'buyinfo_active'
            },
            inplace=True
        )
    elif model == Buy:
        queryset = queryset.annotate(
            buy=F('id'),
        )
        df = read_frame(queryset,
            fieldnames=[
                'buy', 'slug', 'commiter', 'date'
            ]
        )
        df.rename(
            columns={'slug': 'buy_slug', 'date': 'buy_date'}
        )
    elif model == BuyItem:
        queryset = queryset.annotate(
            buy=F('buy_id'), 
            buyinfo=F('buyinfo_id'), 
            buyitem=F('id'),
            product=F('buyinfo__product__id'),
            market=F('buyinfo__market__id'),
            buy_slug=F('buy__slug'),
        )
        df = read_frame(queryset,
            fieldnames=[
                'buyitem', 'buyinfo', 'buy', 'product', 'market',
                'amount', 'comment', 'isend', 'buy_slug'
            ]
        )
        df.rename(
            columns={'amount': 'buyitem_amount'},
            inplace=True
        )
    elif model == StockRecord:
        queryset = queryset.annotate(
            stockrecord=F('id'),
            buyitem=F('buyitem_id'),
            buyinfo=F('buyitem__buyinfo__id'),
            product=F('buyitem__buyinfo__product__id'),
            market=F('buyitem__buyinfo__market__id')
        )
        df = read_frame(queryset, 
            fieldnames=[
                'stockrecord', 'buyitem', 'buyinfo', 'product', 'market',
                'amount', 'date',
            ]
        )
        df.rename(
            columns={'amount': 'stockrecord_amount', 'date': 'stockrecord_date'},
            inplace=True
        )
    else:
        df = read_frame(queryset)

    return df



