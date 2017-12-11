from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from ..models import Market, Product, BuyInfo


class MarketResource(resources.ModelResource):

    class Meta:
        model = Market
        exclude = 'id', 'created',
        import_id_fields = 'name',


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        fields = 'code', 'name', 'company', 'std_unit', 'pkg_amount',
        import_id_fields = 'code', 'name',
        export_order = 'code', 'name', 'company', 'std_unit', 'pkg_amount',


class BuyInfoResource(resources.ModelResource):
    market = fields.Field(
        attribute='market', 
        column_name='market', 
        widget=ForeignKeyWidget(Market,field='name')
    )
    product = fields.Field(
        attribute='product',
        column_name='product',
        widget=ForeignKeyWidget(Product, field='code')
    )

    class Meta:
        model = BuyInfo
        fields = 'market', 'product', 'date', 'price', 'active', 'slug',
        import_id_fields = 'slug',
        export_order = 'market', 'product', 'date', 'price', 'active', 'slug',

