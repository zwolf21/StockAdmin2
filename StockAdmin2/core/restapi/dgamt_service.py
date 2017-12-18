import re, os, sys
from urllib.parse import *
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests, xmltodict
from listorm import Listorm, read_excel

from .settings import RENAMES

API_KEY='zTow8Fpaq1g8Y2mHdZAxWogNcvf9c5DTGNVvVV1tq47bvqUdk9q68QTm2SfteuK4pylybnqEWhi2hMBM5Cc5pQ%3D%3D'


class DGamtService(object):
    API_NAME_URL = {
        'getDgamtList' :'http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getDgamtList',
        'getCmdcDgamtList': 'http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getCmdcDgamtList',
    }

    def __init__(self, api_name='getDgamtList', api_key=API_KEY):
        self.api_name = api_name
        self.api_key = api_key
        self.api_url = self.API_NAME_URL.get(api_name)

    def _response_valid(self, content):
        response = xmltodict.parse(content)
        ret = {}
        try:
            items = response['response']['body']['items']
            totalCount = response['response']['body']['totalCount']
        except:
            raise ValueError('Can not Retrieve response')
        else:
            if items:
                ret = items['item']
                if totalCount in ["1", 1]:
                    return [ret]
                return ret
            else:
                return {}

    def _get(self, **kwargs):
        kwargs['ServiceKey'] = unquote(self.api_key)
        r = requests.get(self.api_url, params=kwargs)
        return r.content

    def getDgamtList(self, renames=RENAMES, **kwargs):
        '''getDgamtList(mdsCd='652600380', itmNm='카리메트')
        '''
        content = self._get(**kwargs)
        records = self._response_valid(content)
        lst = Listorm(records)
        if renames:
            lst = lst.rename(**renames)
        return lst

# api = APIRequest('getDgamtList', api_key)
# lst = api.getDgamtList(mdsCd='652600384')
# pprint(lst.first)


# def check_price_change(edi, price):
#     api = APIRequest('getDgamtList', api_key)
#     lst = api.getDgamtList(mdsCd=edi)
#     if lst:
#         info = lst.first
#         if str(price) != info.mxCprc:
#             return info

# def check_price_change_thread(edi_price_set):
#     max_workers = 5
#     wokers = len(edi_price_set)
#     # args = [(key, val) for key, val in edi_price_set.items()]
#     records = []
#     with ThreadPoolExecutor(min(max_workers, wokers)) as executor:
#         todo_list = [
#             executor.submit(check_price_change, *arg) for arg in edi_price_set
#         ]
#         done_iter = as_completed(todo_list)
#         for future in done_iter:
#             record = future.result()
#             records.append(record)
#     return Listorm(filter(None, records))


# ret=check_price_change('652600384', 631)
# print(ret)
# def ext_edi_price_from_excel(*args, **kwargs):
#     lst = read_excel(*args, **kwargs).select('EDI코드', '보험단가', values=True)
#     return lst

# ediset= ext_edi_price_from_excel('약품정보.xls')
# ediset = {t[0]: t[1] for t in ediset}
# print(ediset[:100])
# ret = check_price_change_thread(ediset[100:150])
# pprint(ret)






