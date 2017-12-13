from pprint import pprint
from ..models import BuyInfo, Market

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .serializers import BuyInfoSerializer


class BuyInfoListAPIView(ListAPIView):
    queryset = BuyInfo.objects.filter(active=True)
    serializer_class = BuyInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = '$product__name', '$market__name',

    def get_queryset(self):
        queryset = super(BuyInfoListAPIView, self).get_queryset()
        market_id = self.kwargs.get('market')
        if market_id:
            return queryset.filter(market__id=market_id)
        return queryset





