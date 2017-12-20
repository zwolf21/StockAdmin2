from django.contrib import admin

from .models import Product, Market, BuyInfo

try:
    from core.imex.admin import ProductImportExportAdmin, MarketImportExportAdmin, BuyInfoImportExportAdmin
except:
    ProductImportExportAdmin = admin.ModelAdmin
    MarketImportExportAdmin = admin.ModelAdmin
    BuyInfoImportExportAdmin = admin.ModelAdmin



@admin.register(Market)
class MarkeAdmin(MarketImportExportAdmin):
    list_display = 'name', 'tel', 'fax', 'email',



class BuyInfoInline(admin.TabularInline):
    model = BuyInfo
    extra = 0

@admin.register(Product)
class ProductAdmin(ProductImportExportAdmin):
    list_display = 'code', 'name','edi_code', 'company', 'std_unit', 'pkg_amount',
    list_filter = 'std_unit', 'etc_class',
    search_fields = 'name', 'company',
    list_editable = 'name', 'company', 'std_unit', 'pkg_amount',
    inlines = BuyInfoInline,



@admin.register(BuyInfo)
class BuyInfoAdmin(BuyInfoImportExportAdmin):
    list_display = 'product', 'market', 'buy_edi_code', 'pay_type', 'pro_type', 'buy_edi_code', 'date', 'price', 'active',
    list_filter = 'market', 'pay_type', 'pro_type', 'active', 'product__std_unit', 'date',
    search_fields = 'product__name',
    autocomplete_fields = 'product',