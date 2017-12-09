from django.contrib import admin

from .models import Product, Market


@admin.register(Market)
class MarkeAdmin(admin.ModelAdmin):
    list_display = 'name', 'tel', 'fax', 'email',


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'company', 'std_unit', 'pkg_amount',
    list_filter = 'std_unit',
    search_fields = 'name', 'company',
    list_editable = 'name', 'company', 'std_unit', 'pkg_amount',
