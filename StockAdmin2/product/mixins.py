from django.core.exceptions import ValidationError
from django.db.models import Q

from utils.shortcuts import sequence_fk_slugify

class BuyInfoMixin(object):

    def save(self, **kwargs):
        if not self.id:
            previous = self.product.buyinfo_set.all()
            if self.active == True:
                self.product.buyinfo_set.filter(market=self.market).update(active=False)
        else:
            if self.active == True:
                queryset = self.product.buyinfo_set.filter(market=self.market)
                queryset = queryset.exclude(id=self.id)
                queryset.update(active=False)


        if not self.slug:
            self.slug = sequence_fk_slugify(self, 'product', 'code')

        return super(BuyInfoMixin, self).save(**kwargs)

