from django.db import models



class StockRecordManager(models.Manager):

    def create_dummy(self, buyitem):
        if buyitem:
            queryset = self.get_queryset()
            stockrecord_set = self.buyitem.stockrecord_set
            dummy = stockrecord_set.filter(amount=0)
            if not buyitem.iscompleted:
                if not dummy.exists():
                    self.create(buyitem=buyitem, amount=0)
            else:
                if dummy.exists():
                    dummy.delete()