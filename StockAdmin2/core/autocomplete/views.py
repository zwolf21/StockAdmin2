from pprint import pprint
from ..models import BuyInfo, Market, BuyItem

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
        slug = self.kwargs.get('slug')

        market = None
        if slug:
            buyitem_set = BuyItem.objects.filter(buy__slug=slug)
            if buyitem_set.exists():
                market = buyitem_set.first().buyinfo.market
        else:
            buyitem_set = BuyItem.objects.filter(buy__isnull=True)

        queryset = queryset.exclude(buyitem__in=buyitem_set)

        if market:
            queryset = queryset.filter(market=market)

        return queryset





