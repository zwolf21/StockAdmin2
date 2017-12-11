from django.contrib import admin

from .models import Buy, BuyItem


class BuyItemInline(admin.TabularInline):
    model = BuyItem
    extra = 0


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = 'slug', 'date', 'commiter',
    inlines = BuyItemInline,    


@admin.register(BuyItem)
class BuyItemAdmin(admin.ModelAdmin):
    list_display = 'buy', 'buyinfo', 'amount', 'isend',
    list_filter = 'buy', 'isend',
    list_search = 'buyinfo__product__name',
    search_fields = 'buyinfo__product__name',