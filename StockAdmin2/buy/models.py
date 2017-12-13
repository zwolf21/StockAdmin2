from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from utils.shortcuts import sequence_date_slugify



class Buy(models.Model):
    slug = models.SlugField('구매번호', unique=True, blank=True, editable=False)
    commiter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField('구매일자', blank=True, default=timezone.now)
    iscart = models.BooleanField('카트인지', blank=True, default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '구매요청서'
        verbose_name_plural = '구매요청서'
        ordering = '-created', 

    def __str__(self):
        return self.slug

    def save(self, **kwargs):
        if not self.slug:
            self.slug = sequence_date_slugify(self, 'date')
        return super(Buy, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('buy:buy-detail', args=(self.slug,))

    @property
    def description(self):
        itemset = self.buyitem_set.all()
        if itemset.exists():
            fistitem = str(itemset.first().buyinfo)
            count = itemset.count()
            return "{} 등 {}건".format(fistitem, count)
        return "내역없음"



class BuyItem(models.Model):
    buy = models.ForeignKey(Buy, null=True, blank=True, on_delete=models.CASCADE)
    buyinfo = models.ForeignKey('product.BuyInfo', on_delete=models.CASCADE)
    amount = models.IntegerField('구매수량')
    comment = models.CharField('비고', max_length=50, blank=True)
    isend = models.BooleanField('구매종결', default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '구매품목'
        verbose_name_plural = '구매품목'
        unique_together = 'buy', 'buyinfo',

    def __init__(self, *args, **kwargs):
        super(BuyItem, self).__init__(*args, **kwargs)

    def __str__(self):
        return str(self.buyinfo)

    def get_stocked_sum(self):
        aggset = self.stockrecord_set.aggregate(stocked=Sum('amount'))
        return aggset['stocked'] or 0



class StockRecord(models.Model):
    buyitem = models.ForeignKey(BuyItem, on_delete=models.CASCADE)
    date = models.DateField('입고일자', blank=True, null=True)
    amount = models.IntegerField('입고수량', default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '입고기록'
        verbose_name = '입고기록'
        ordering = '-buyitem__created',

    def __str__(self):
        return str(self.buyitem)

    def __init__(self, *args, **kwargs):
        super(StockRecord, self).__init__(*args, **kwargs)
        self.old_amount  = self.amount

    def create_for_stock(self):
        stockrecord_set = self.buyitem.stockrecord_set
        if stockrecord_set.filter(amount=0).exists():
            return
        stocked_amount = self.buyitem.get_stocked_sum()
        if self.buyitem.amount > stocked_amount:
            stockrecord_set.create()

    def clean(self):
        stockrecord_set = self.buyitem.stockrecord_set
        if self.id:
            stocked_amount = self.buyitem.get_stocked_sum()
            new_amount = stocked_amount - self.old_amount + self.amount
            if new_amount > self.buyitem.amount:
                raise ValidationError('입고수량이 구매수량을 초과 합니다')



@receiver(post_save, sender=BuyItem)
def buyitem_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.stockrecord_set.create()


@receiver(post_save, sender=StockRecord)
def stockrecord_post_save(sender, instance, created, *args, **kwargs):
    instance.create_for_stock()





