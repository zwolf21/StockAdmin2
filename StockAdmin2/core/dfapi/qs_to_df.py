from django_pandas.io import read_frame
from django.db.models import F

from ..models import *


def queryset_to_dataframe(queryset):
    model = queryset.model

    if model == Market:
        queryset = queryset.annotate(id_market=F('id'))
        df = read_frame(queryset,
            fieldnames=['id_market', 'name']
        )
        df.rename(
            columns={'name': 'market_name'},
            inplace=True
        )
    elif model == Product:
        queryset = queryset.annotate(id_product=F('id'))
        df = read_frame(queryset,
            fieldnames=[
                'id_product',
                'code', 'name', 'company', 'std_unit', 'pkg_amount', 'etc_class'
            ]
        )
        df.rename(
            columns={'code': 'product_code', 'name': 'product_name'},
            inplace=True
        )
    elif model == BuyInfo:
        queryset = queryset.annotate(
            id_buyinfo=F('id'),
            id_product=F('product_id'),
            id_market=F('market_id')
        )
        df = read_frame(queryset,
            fieldnames=[
                'id_buyinfo', 'id_market', 'id_product',
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
            id_buy=F('id'),
        )
        df = read_frame(queryset,
            fieldnames=[
                'id_buy', 'slug', 'commiter', 'date'
            ]
        )
        df.rename(
            columns={'slug': 'buy_slug', 'date': 'buy_date'}
        )
    elif model == BuyItem:
        queryset = queryset.annotate(
            id_buy=F('buy_id'), 
            id_buyinfo=F('buyinfo_id'), 
            id_buyitem=F('id'),
            id_product=F('buyinfo__product__id'),
            id_market=F('buyinfo__market__id'),
            buy_slug=F('buy__slug'),
        )
        df = read_frame(queryset,
            fieldnames=[
                'id_buyitem', 'id_buyinfo', 'id_buy', 'id_product', 'id_market',
                'amount', 'comment', 'isend', 'buy_slug'
            ]
        )
        df.rename(
            columns={'amount': 'buyitem_amount'},
            inplace=True
        )
    elif model == StockRecord:
        queryset = queryset.annotate(
            id_stockrecord=F('id'),
            id_buyitem=F('buyitem_id'),
            id_buyinfo=F('buyitem__buyinfo__id'),
            id_product=F('buyitem__buyinfo__product__id'),
            id_market=F('buyitem__buyinfo__market__id')
        )
        df = read_frame(queryset, 
            fieldnames=[
                'id_stockrecord', 'id_buyitem', 'id_buyinfo', 'id_product', 'id_market',
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



