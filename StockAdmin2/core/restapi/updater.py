from decimal import Decimal
from listorm import Listorm

from .dgamt_service import DGamtService

update_supervise_fields = {
    'edi_code':'update', 'pro_type':'update', 'pay_type':'update',
    'price':'create'
}

product_supervise_fields = {
    'edi_code': 'update'
}

buyinfo_supervise_field = {
    'pro_type': 'update', 'pay_type': 'update',
    'price':'create', 'buy_edi_code': 'create'
}

# update: 변경시 레코드 항목 수정만하기 create: 변경사항 발생시 새로 만들기
UPDATE_METHOD = {
    'product': {
        'update': [
            'edi_code', 'unit', 'company', 'unit_amount', 'apply_root', 'op_type'
        ],
    },
    'buyinfo': {
        'create': ['buy_edi_code', 'price'], 
        'update': ['pro_type', 'pay_type', 'date']
    }
}



def get_newest_record(edi_code, recursive_try=5):
    if recursive_try == 0:
        return edi_code

    if not edi_code:
        return

    api = DGamtService()
    api_lst = api.getDgamtList(mdsCd=edi_code)
    if len(api_lst) == 1:
        record = api_lst.first
        if record.edi_code_after:
            return get_newest_record(
                record.edi_code_after,
                recursive_try=recursive_try-1
            )
        return record  



def get_fieldset_for_update(instance, new_record, update_methods=UPDATE_METHOD):
    instance_name = instance.__class__.__name__.lower()    
    update_context = update_methods.get(instance_name, {})
    updates, creates = {}, {}
    for method, fields in update_context.items():
        for field in fields:
            oldVal = str(getattr(instance, field) or '')
            newVal = str(getattr(new_record, field) or '')
            if not newVal:
                continue
            if oldVal != newVal:
                if method == 'update':
                    updates[field] = newVal
                else:
                    create[field] = newVal
    return creates, updates


def record_isvalid(record):
    if record.get('price') not in [0, '0', '', None]:
        return True
    return False



def smart_update(product, update_methods=UPDATE_METHOD):
    new_record = get_newest_record(product.edi_code)
    if not new_record:
        return

    new_edi_code = new_record.get('edi_code')

    if new_edi_code != product.edi_code:
        product.edi_code = new_edi_code
        product.save()

    product_creates, product_updates = get_fieldset_for_update(product, new_record)
    product.__class__.objects.filter(pk=product.id).update(**product_updates)

    buyinfo_set = product.buyinfo_set.filter(buy_edi_code=new_edi_code, active=True)
    new_price = Decimal(new_record.price or 0)

    if product.buyinfo_set.exists():
        market = product.buyinfo_set.last().market
    else:
        market = None

    buyinfo_create_fields = update_methods.get('buyinfo', {}).get('create', [])
    buyinfo_update_fields = update_methods.get('buyinfo', {}).get('update', [])
    buyinfo_create_kwargs = new_record.select(*(buyinfo_create_fields+buyinfo_update_fields), values=False)
    buyinfo_update_kwargs = new_record.select(*buyinfo_update_fields, values=False)
    buyinfo_create_kwargs['product'] = product
    buyinfo_update_kwargs['product'] = product

    if not buyinfo_set.exists():
        if not new_price:
            print(new_price)
            buyinfo_create_kwargs['price'] = 0
        buyinfo_set.create(**buyinfo_create_kwargs)
    else:
        buyinfo_create_kwargs['market'] = market
        buyinfo_update_kwargs['market'] = market
        if new_price: 
            buyinfo_set = buyinfo_set.filter(price=new_price)
            if not buyinfo_set.exists():
                buyinfo_set.create(**buyinfo_create_kwargs)
            else:
                buyinfo_set.update(**buyinfo_update_kwargs)
        else:
            buyinfo_update_kwargs.pop('price')
            buyinfo_set.update(**buyinfo_update_kwargs)












    