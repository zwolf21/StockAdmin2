from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

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
        return reverse('buy:detail', args=(self.slug,))

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
    buyinfo = models.ForeignKey('product.BuyInfo', on_delete=models.PROTECT)
    amount = models.IntegerField('구매수량')
    comment = models.CharField('비고', max_length=50, blank=True)
    isend = models.BooleanField('구매종결', default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '구매품목'
        verbose_name_plural = '구매품목'
        unique_together = 'buy', 'buyinfo',

    def __str__(self):
        return str(self.buyinfo)