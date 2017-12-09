from django.db import models
from django.utils import timezone

from .mixins import BuyInfoMixin


class Market(models.Model):
    name = models.CharField('도매상명', max_length=50, unique=True)
    tel = models.CharField('전화', max_length=50, blank=True, null=True)
    fax = models.CharField('팩스', max_length=50, blank=True, null=True)
    email = models.EmailField('메일', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '도매상'
        verbose_name_plural = '도매상'

    def __str__(self):
        return self.name



STD_UNITs = 'TAB', 'CAP', 'VIAL', 'AMP', 'TUBE', 'SYR', 'PEN', 'BTL', 'BAG', '포',
ETC_CLASS = '일반', '항암제', '마약', '향정', '수액', '영양수액', '인슐린주사', '백신', '조영제', '처치약품', '소모품', '직송'

class Product(models.Model):
    name = models.CharField('제품명', max_length=50, unique=True)
    code = models.CharField('제품코드', max_length=50, unique=True)
    company = models.CharField('판매사', max_length=50, blank=True)
    std_unit = models.CharField('제품규격', max_length=10, choices=zip(STD_UNITs, STD_UNITs))
    pkg_amount = models.IntegerField('포장수량', default=1)
    etc_class = models.CharField('기타구분', max_length=10, choices=zip(ETC_CLASS, ETC_CLASS), default='일반')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '제품'
        verbose_name_plural = '제품'
        ordering = '-created',

    def __str__(self):
        return self.name

   
class BuyInfo(BuyInfoMixin, models.Model):
    slug = models.SlugField('구매코드', unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    date = models.DateField('시작일자', blank=True, default=timezone.now)
    price = models.DecimalField('구매가격', max_digits=50, decimal_places=2)
    active = models.BooleanField('사용중', default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '구매정보'
        verbose_name_plural = '구매정보'
        ordering = '-created',

    def __str__(self):
        title = "{}-{}({:,.0f}원)".format(self.product.name, self.market.name, self.price)
        return title






