from .qs_to_df import queryset_to_dataframe

from ..models import *


class QuerySetDataFrame:

    def __init__(self, queryset):
        self.model = queryset.model
        self._load_base_df()
        record_df = queryset_to_dataframe(queryset)
        self.df = record_df.merge(self.buyinfo_df).merge(self.product_df).merge(self.market_df)


    def _load_base_df(self):
        self.market_df = queryset_to_dataframe(Market.objects.all())
        self.product_df = queryset_to_dataframe(Product.objects.all())
        self.buyinfo_df = queryset_to_dataframe(BuyInfo.objects.all())


    def annotate(self, group_field):
        df = self.df.copy()
        group_key = "id_{}".format(group_field.lower())
        if self.model == BuyItem:
            df['buy_price'] = df['price'] * df['buyitem_amount']
            aggset = [
                ('buy_amount_sum', 'buyitem_amount', 'sum'),
                ('buy_price_sum', 'buy_price', 'sum'),
                ('buy_count', 'id_buyitem', 'count')
            ]
        elif self.model == StockRecord:
            df['stock_price'] = df['price'] * df['stockrecord_amount']
            aggset = [
                ('stocked_amount_sum', 'stockrecord_amount', 'sum'),
                ('stocked_price_sum', 'stock_price', 'sum')
            ]
        else:
            return df

        for colname, aggcol, aggfunc in aggset:
            df[colname] = df.groupby(group_key)[aggcol].transform(aggfunc)

        df.drop_duplicates(group_key, inplace=True)
        return df


def df_to_records(df):
    return df.to_dict('record')




