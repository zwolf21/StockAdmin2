from django.db import models
from django.db.models import *



class BuyItemQuerySet(models.QuerySet):

    def get_valid_set(self):
        return self.filter(buy__isnull=False, buy__commiter__isnull=False)

    def annotate_fk(self):
        return self.annotate(
            id_buy=F('buy_id'), 
            id_buyinfo=F('buyinfo_id'), 
            id_buyitem=F('id'),
            id_product=F('buyinfo__product__id'),
            id_market=F('buyinfo__market__id')
        )


    def group_by_fk(self, model_name, get_total_price=True):
        qs = self.get_valid_set()

        if model_name == 'Product':
            group_key = 'buyinfo__product'
            groupedset = qs.order_by(group_key).values(group_key).annotate(
                product_code=F('buyinfo__product__code'),
                product_name=F('buyinfo__product__name'),
                market_name=F('buyinfo__market__name'),
                price=F('buyinfo__price'),
                buy_amount_sum=Sum('amount'),
                buy_count=Count('id'),
                buy_price_sum=Sum(F('buyinfo__price')*F('amount'), output_field=IntegerField())
            )
        elif model_name == 'BuyInfo':
            group_key = 'buyinfo'
            groupedset = qs.order_by(group_key).values(group_key).annotate(
                buyinfo_slug=F('buyinfo__slug'),
                product_name=F('buyinfo__product__name'),
                market_name=F('buyinfo__market__name'),
                price=F('buyinfo__price'),
                buy_amount_sum=F('amount'),
                buyitem_count=Count('id'),
                buy_price_sum=Sum(F('buyinfo__price')*F('amount'), output_field=IntegerField())
            )
        elif model_name == 'Market':
            group_key = 'buyinfo__market'
            groupedset = qs.order_by(group_key).values(group_key).annotate(
                market_name=F('buyinfo__market__name'),
                buy_count=Count('buy', distinct=True),
                buyitem_count=Count('id'),
                buy_price_sum=Sum(F('buyinfo__price')*F('amount'), output_field=IntegerField())
            )
        else:
            groupedset = qs.annotate(
                stocked_amount_sum=Sum('stockrecord__amount'),
                stock_status=Case(
                    When(amount=F('stocked_amount_sum'), then=Value('완료')),
                    When(isend=True, then=Value('종결')),
                        default=Value('입고중'),
                        output_field=CharField()
                    ),
                buy_price_sum=ExpressionWrapper(
                    F('buyinfo__price')*F('amount'), output_field=IntegerField()
                ),
                stocked_price_sum=ExpressionWrapper(
                    F('buyinfo__price')*F('stocked_amount_sum'), output_field=IntegerField()
                )

            )
        if get_total_price == False:
            return groupedset

        aggset = groupedset.aggregate(
            total_price=Sum('buy_price_sum', output_field=IntegerField())
        )
        return groupedset, aggset['total_price'] or 0




class BuyItemManager(models.Manager):

    def get_queryset(self):
        return BuyItemQuerySet(self.model, using=self._db)



class StockRecordQuerySet(models.QuerySet):

    def get_valid_set(self):
        return self.filter(amount__gt=0)

    def annotate_fk(self):
        return self.annotate(
            id_stockrecord=F('id'),
            id_buyitem=F('buyitem_id'),
            id_buyinfo=F('buyitem__buyinfo__id'),
            id_product=F('buyitem__buyinfo__product__id'),
            id_market=F('buyitem__buyinfo__market__id')
        )

    def group_by_fk(self, model_name=None, get_total_price=True):
        qs = self.get_valid_set()

        if model_name == 'Product':
            group_key = 'buyitem__buyinfo__product'
            groupedset = qs.order_by(group_key).values(group_key).annotate(
                product_code=F('buyitem__buyinfo__product__code'),
                product_name=F('buyitem__buyinfo__product__name'),
                first_stocked_date=Min('date'),
                last_stocked_date=Max('date'),
                stocked_amount_sum=Sum('amount'),
                stocked_price_sum=Sum(
                    F('buyitem__buyinfo__price')*F('amount'),
                    output_field=IntegerField()
                )
            )
        elif model_name == 'BuyInfo':
            group_key = 'buyitem__buyinfo'
            groupedset = qs.order_by(group_key).values(group_key).annotate(
                market_name=F('buyitem__buyinfo__market__name'),
                buy_price=F('buyitem__buyinfo__price'),
                product_code=F('buyitem__buyinfo__product__code'),
                product_name=F('buyitem__buyinfo__product__name'),
                first_stocked_date=Min('date'),
                last_stocked_date=Max('date'),
                stocked_amount_sum=Sum('amount'),
                stocked_price_sum=Sum(
                    F('buy_price')*F('amount'), output_field=IntegerField()
                )
            )
        elif model_name == 'Market':
            group_key = 'buyitem__buyinfo__market'
            groupedset = qs.order_by(group_key).values(group_key).annotate(
                market_name=F('buyitem__buyinfo__market__name'),
                first_stocked_date=Min('date'),
                last_stocked_date=Max('date'),
                stocked_count=Count(group_key),
                stocked_price_sum=Sum(
                    F('buyitem__buyinfo__price')*F('amount'),
                    output_field=IntegerField()
                )
            )
        else:
            groupedset = qs.annotate(
                buy_price=F('buyitem__buyinfo__price'),
                stocked_price_sum=ExpressionWrapper(
                    F('buyitem__buyinfo__price')*F('amount'),
                    output_field=IntegerField()
                )
            )

        if get_total_price == False:
            return groupedset

        aggset = groupedset.aggregate(
            total_price=Sum('stocked_price_sum', output_field=IntegerField())
        )
        return groupedset, aggset['total_price'] or 0



class StockRecordManager(models.Manager):

    def get_queryset(self):
        return StockRecordQuerySet(self.model, using=self._db)

