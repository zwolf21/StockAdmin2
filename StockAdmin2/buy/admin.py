from django.contrib import admin

from .models import Buy, BuyItem

@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    pass
    