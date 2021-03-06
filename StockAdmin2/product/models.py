from django.db import models
from django.utils import timezone
from django.urls import reverse

from .mixins import BuyInfoMixin
from .managers import MarketManager, ProductManager, BuyInfoManager


class Market(models.Model):
    name = models.CharField('도매상명', max_length=50, unique=True)
    tel = models.CharField('전화', max_length=50, blank=True, null=True)
    fax = models.CharField('팩스', max_length=50, blank=True, null=True)
    email = models.EmailField('메일', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = MarketManager()

    class Meta:
        verbose_name = '거래처'
        verbose_name_plural = '거래처'

    def __str__(self):
        return self.name



STD_UNITs = [
    'TAB', 'CAP', 'VIAL', 'AMP', 'BTL', 'EA', 'ML', 'SYR', 'BAG', '포', '통',
    '매', 'PEN', 'G', '관', 'PKG', 'POWD', 'FILM', 'KIT', 'SC', 'GRAN', 'SET',
    'IU', 'PFS', 'SUPP', 'GEL', 'TUBE'
]
ETC_CLASS = '일반', '항암제', '마약', '향정', '수액', '영양수액', '인슐린주사', '백신', '조영제', '처치약품', '소모품', '직송'


class Product(models.Model):
    name = models.CharField('제품명', max_length=50, unique=True)
    code = models.CharField('제품코드', max_length=50, unique=True)
    edi_code = models.CharField('보험코드', max_length=50, blank=True, default="")
    company = models.CharField('판매사', max_length=50, blank=True, default="")
    std_unit = models.CharField('제품규격', max_length=10, choices=zip(STD_UNITs, STD_UNITs), default="")
    pkg_amount = models.IntegerField('포장수량', default=1)
    etc_class = models.CharField('기타구분', max_length=10, choices=zip(ETC_CLASS, ETC_CLASS), default='일반')
    apply_root = models.CharField('복용방법', max_length=50, blank=True, default="")
    unit = models.CharField('적용단위', max_length=50, blank=True, default="")
    unit_amount = models.CharField('규격단위량', max_length=50, blank=True, default="")

    op_type = models.CharField('마약류구분', blank=True, max_length=50, default="")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    class Meta:
        verbose_name = '제품'
        verbose_name_plural = '제품'
        ordering = '-created',

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:detail', args=(self.pk,))


   
class BuyInfo(BuyInfoMixin, models.Model):
    slug = models.SlugField('구매코드', unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True, blank=True)
    buy_edi_code = models.CharField('보험코드', max_length=50, blank=True, default="")
    date = models.DateField('시작일자', blank=True, default=timezone.now)
    price = models.DecimalField('구매가격', max_digits=50, decimal_places=2, default=0)
    pay_type = models.CharField('급여구분', blank=True, max_length=50, default="")
    pro_type = models.CharField('전문/일반', blank=True, max_length=50, default="")
    active = models.BooleanField('사용중', default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = BuyInfoManager()

    class Meta:
        verbose_name = '구매정보'
        verbose_name_plural = '구매정보'
        ordering = '-created',

    def __str__(self):
        if self.market and self.product:
            title = "{}-{}({:,.0f}원)".format(self.product.name, self.market.name, self.price)
            return title
        return self.slug






