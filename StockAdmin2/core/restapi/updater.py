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
    'pro_type': 'update', 'pay_type': 'update', 'price':'create'
}






def update_from_rest_api(product, recursive=5):
    if recursive == 0:
        return 

    edi_code = product.edi_code
    if not edi_code:
        return

    api = DGamtService()
    api_lst = api.getDgamtList(mdsCd=edi_code)
    api_lst = api_lst.set_number_type(price=0)

    if not api_lst:
        return

    sch = api_lst.first

    if sch.edi_code_after:
        product.edi_code = sch.edi_code_after
        product.save()
        return update_from_rest_api(product, recursive=recursive-1)

    buyinfo_set = product.buyinfo_set.filter(active=True)
    fields_for_create = sch.select(*buyinfo_supervise_field, values=False)

    if not buyinfo_set.exists():
        buyinfo_set.create(product=product, **fields_for_create)
    else:
        don_need_to_create = False
        for buyinfo in buyinfo_set:
            for field, how in buyinfo_supervise_field.items():
                ori_val = str(getattr(buyinfo, field))
                api_val = str(getattr(sch, field))
                if ori_val != api_val:
                    if how == 'update' and api_val:
                        setattr(buyinfo, field, api_val)
                        buyinfo.save()

                if ori_val == api_val and how=='create' and api_val:
                    don_need_to_create = True
        
        if don_need_to_create == False:
            print('creating buyinfo...', product)
            market = buyinfo_set.filter(market__isnull=False).last().market
            buyinfo_set.create(product=product, market=market, **fields_for_create)
    return True











    