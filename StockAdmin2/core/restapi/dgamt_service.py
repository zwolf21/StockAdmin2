import re, os, sys
from urllib.parse import *
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests, xmltodict
from listorm import Listorm, read_excel
from dateutil.parser import parse

from .settings import RENAMES
from django.conf import settings



class DGamtService(object):
    API_NAME_URL = {
        'getDgamtList' :'http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getDgamtList',
        'getCmdcDgamtList': 'http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getCmdcDgamtList',
    }

    def __init__(self, api_name='getDgamtList', api_key=settings.DGAMT_API_KEY):
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
            # raise ValueError('Can not Retrieve response')
            print(response)
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
            lst = lst.add_columns(buy_edi_code=lambda row:row.edi_code)
            lst = lst.update(date=lambda row: parse(row.date))
        return lst


