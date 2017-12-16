from django.db import models
from django.db.models import *



class MarketQuerySet(models.QuerySet):

    def get_valid_stockrecord_set(self):
        return self.filter(buyinfo__buyitem__stockrecord__amount__gt=0)

    def annotate_stockrecord(self, aggset=False):
        annoset = self.get_valid_stockrecord_set().annotate(
            first_stocked_date=Min('buyinfo__buyitem__stockrecord__date'),
            last_stocked_date=Max('buyinfo__buyitem__stockrecord__date'),
            stocked_count=Count(Case(When(buyinfo__buyitem__stockrecord__amount__gt=0, then=1))),
            stocked_amount_sum=Sum('buyinfo__buyitem__stockrecord__amount'),
            stocked_price_sum=Sum(
                F('buyinfo__price')*F('buyinfo__buyitem__stockrecord__amount'),
                output_field=IntegerField()
            )
        )
        if aggset == False:
            return annoset
        aggset = annoset.aggregate(stocked_price_total=Sum('stocked_price_sum'))
        return {'annoset': annoset, 'aggset': aggset}



class MarketManager(models.Manager):

    def get_queryset(self):
        return MarketQuerySet(self.model, using=self._db)

        

class ProductQuerySet(models.QuerySet):

    def get_valid_stockrecord_set(self):
        return self.filter(buyinfo__buyitem__stockrecord__amount__gt=0)

    def annotate_stockrecord(self, aggset=False):
        annoset = self.get_valid_stockrecord_set().annotate(
            first_stocked_date=Min('buyinfo__buyitem__stockrecord__date'),
            last_stocked_date=Max('buyinfo__buyitem__stockrecord__date'),
            # stocked_count=Count(Case(When(buyinfo__buyitem__stockrecord__amount__gt=0, then=1))),
            stocked_amount_sum=Sum('buyinfo__buyitem__stockrecord__amount', distinct=True),
            stocked_price_sum=Sum(
                F('buyinfo__buyitem__stockrecord__amount'),
                output_field=IntegerField()
            )
        )
        if aggset == False:
            return annoset
        aggset = annoset.aggregate(stocked_price_total=Sum('stocked_price_sum'))
        return {'annoset': annoset, 'aggset': aggset}



class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)



class BuyInfoQuerySet(models.QuerySet):

    def get_valid_stockrecord_set(self):
        return self.filter(buyitem__stockrecord__amount__gt=0)

    def annotate_stockrecord(self, aggset=False):
        annoset = self.get_valid_stockrecord_set().annotate(
            first_stocked_date=Min('buyitem__stockrecord__date'),
            last_stocked_date=Max('buyitem__stockrecord__date'),
            stocked_count=Count(Case(When(buyitem__stockrecord__amount__gt=0, then=1))),
            stocked_amount_sum=Sum('buyitem__stockrecord__amount'),
            stocked_price_sum=Sum(
                F('price')*F('buyitem__stockrecord__amount'),
                output_field=IntegerField()
            )
        )
        if aggset == False:
            return annoset
        aggset = annoset.aggregate(stocked_price_total=Sum('stocked_price_sum'))
        return {'annoset': annoset, 'aggset': aggset}


class BuyInfoManager(models.Manager):

    def get_queryset(self):
        return BuyInfoQuerySet(self.model, using=self._db)












