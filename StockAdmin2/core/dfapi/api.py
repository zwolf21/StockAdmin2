from .qs_to_df import queryset_to_dataframe

from ..models import *


class BuyItemQuerySetDataFrame:

    def __init__(self, buyitem_set):
        # self.model = buyitem_set.model
        # self.buyitem_set = buyitem_set
        # self.stockrecord_set = StockRecord.objects.filter(buyitem__in=buyitem_set)
        # self._load_base_df()
        # record_df = queryset_to_dataframe(buyitem_set)
        # self.stkrc_df = queryset_to_dataframe(stockrecord_set)
        # self.df = record_df.merge(self.buyinfo_df).merge(self.product_df).merge(self.market_df)


        self._load_base_df()
        df = self._merge_stockrecord(buyitem_set)
        self.df = df.merge(self.buyinfo_df).merge(self.product_df).merge(self.market_df)

    def _load_base_df(self):
        self.market_df = queryset_to_dataframe(Market.objects.all())
        self.product_df = queryset_to_dataframe(Product.objects.all())
        self.buyinfo_df = queryset_to_dataframe(BuyInfo.objects.all())

    def _merge_stockrecord(self, buyitem_set):
        stockrecord_set=StockRecord.objects.filter(buyitem__in=buyitem_set)
        bdf = queryset_to_dataframe(buyitem_set)
        sdf = queryset_to_dataframe(stockrecord_set)

        agg_list = [
            ('stockrecord_amount_sum', 'stockrecord_amount', 'sum'),
            ('stockrecord_count', 'stockrecord', 'count'),
        ]
        aggset = {}
        for label, column, func in agg_list:
            sdf[label] = sdf[column]
            aggset[label] = func

        sdf=sdf.groupby('buyitem').agg(aggset)
        df = bdf.merge(sdf, how='left')

        #annotate etc
        df['is_completed'] = (df.stocked_amount_sum==df.buyitem_amount)
        df.loc[df['is_completed']==False, ['is_completed']] = df.isend

        return df


    def transform(self, key):
        df = self.df.copy()
        key = key.lower()

        agg_list = [
            ('buyitem_amount_sum', 'buyitem_amount', 'sum'),
            ('completed_count', 'is_completed', 'count'),
        ]
        for label, column, func in agg_list:
            df[label] = df.groupby(key)[column].transform(func)






    def annotate(self, group_field):
        df = self.df.copy()
        group_key = "{}".format(group_field.lower())
        if self.model == BuyItem:
            df['buy_price'] = df['price'] * df['buyitem_amount']
            aggset = [
                ('buy_amount_sum', 'buyitem_amount', 'sum'),
                ('buy_price_sum', 'buy_price', 'sum'),
                ('buyitem_count', 'id_buyitem', 'count')
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

def merge_buyitem_with_stockrecord(buyitemset):



def df_to_records(df):
    return df.to_dict('record')





























