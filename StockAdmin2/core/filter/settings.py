from django.utils import timezone

DATE_PERIOD = 14
START_DATE_INI = timezone.now() - timezone.timedelta(DATE_PERIOD)
END_DATE_INI = timezone.now() 


DATE_KEYWORD_SET = {
    '어제', 'ㅇㅈ', '오늘', 'ㅇㄴ', '그제', 'ㄱㅈ', '내일', 'ㄴㅇ'
}

LOOKUP_CONTEXTS = {
    'StockRecord-stocked': {
        'date_range': [
            'date',
        ],
        'contains': [
            'buyitem__buyinfo__product__name',
            'buyitem__buyinfo__product__company',
        ],
        'slug': [
            'buyitem__buy__slug',
        ],
        'etc_class': [
            'buyitem__buyinfo__product__etc_class',
        ],
        'market': [
            'buyitem__buyinfo__market__name',
        ]
    },
    'StockRecord-stocking': {
        'date_range': [
            'buyitem__buy__date',
        ],
        'contains': [
            'buyitem__buyinfo__product__name',
            'buyitem__buyinfo__product__company',
        ],
        'slug': [
            'buyitem__buy__slug',
        ],
        'etc_class': [
            'buyitem__buyinfo__product__etc_class',
        ],
        'market': [
            'buyitem__buyinfo__market__name',
        ]
    },
    'BuyItem': {
        'date_range': [
            'buy__date',
        ],
        'contains': [
            'buyinfo__product__name',
            'buyinfo__product__company',
        ],
        'slug': [
            'buy__slug',
        ],
        'etc_class': [
            'buyinfo__product__etc_class'
        ],
        'market': [
            'buyinfo__market__name',
        ]
    },
    'Product': {
        'contains': [
            'name', 'company'
        ],
        'market': [
            'buyinfo__market__name',
        ],
        'etc_class': [
            'etc_class'
        ]
    }
}
