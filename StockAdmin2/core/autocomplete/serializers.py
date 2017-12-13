from ..models import BuyInfo, Market

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class BuyInfoSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    pkg_amount = serializers.SerializerMethodField()
    market_name = serializers.SerializerMethodField()

    class Meta:
        model = BuyInfo
        fields = 'label', 'value', 'id', 'pkg_amount', 'market_name', 'name'

    def get_label(self, instance):
        return str(instance)

    def get_name(self, instance):
        return self.get_label(instance)

    def get_value(self, instance):
        return str(instance)

    def get_pkg_amount(self, instance):
        return instance.product.pkg_amount

    def get_market_name(self, instance):
        return instance.market.name
