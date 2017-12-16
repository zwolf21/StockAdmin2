from django.db import models
from django.db.models import *



class StockRecordQuerySet(models.QuerySet):

    def get_valid_set(self):
        return self.filter(amount__gt=0)

    def annotate_stockrecord(self, aggset=False):
        annoset = self.get_valid_set().annotate(
            buy_price=F('buyitem__buyinfo__price'),
            stocked_price_sum=Sum(
                F('buy_price')*F('amount'),
                output_field=IntegerField()
            ),
        )
        if aggset == False:
            return annoset
        aggset = annoset.aggregate(stocked_price_total=Sum('stocked_price_sum'))
        return {'annoset': annoset, 'aggset': aggset}




class StockRecordManager(models.Manager):

    def get_queryset(self):
        return StockRecordQuerySet(self.model, using=self._db)

    # def create_dummy(self, buyitem):
    #     if buyitem:
    #         queryset = self.get_queryset()
    #         stockrecord_set = self.buyitem.stockrecord_set
    #         dummy = stockrecord_set.filter(amount=0)
    #         if not buyitem.iscompleted:
    #             if not dummy.exists():
    #                 self.create(buyitem=buyitem, amount=0)
    #         else:
    #             if dummy.exists():
    #                 dummy.delete()