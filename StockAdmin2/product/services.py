from core.restapi import update_from_rest_api, smart_update


def update_info_by_api(product):
    # return update_from_rest_api(product)
    return smart_update(product)


