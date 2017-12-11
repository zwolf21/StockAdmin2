from import_export.admin import ImportExportModelAdmin

from .resources import BuyInfoResource, MarketResource, ProductResource



class MarketImportExportAdmin(ImportExportModelAdmin):
    resource_class = MarketResource


class ProductImportExportAdmin(ImportExportModelAdmin):
    resource_class = ProductResource


class BuyInfoImportExportAdmin(ImportExportModelAdmin):
    resource_class = BuyInfoResource
