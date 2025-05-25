import requests
from dotenv import load_dotenv
import os
from django.conf import settings
from rest_framework.decorators import api_view

load_dotenv()

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

def api_call():
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': os.getenv("API_KEY"),           # .env 파일에 API_KEY 설정 필요
        'topFinGrpNo': '020000',            # 금융회사 코드 (은행)
        'pageNo': 1
    }
    
    deposit_response = requests.get(URL, params=params).json()
    
    URL = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth': os.getenv("API_KEY"),           # .env 파일에 API_KEY 설정 필요
        'topFinGrpNo': '020000',            # 금융회사 코드 (은행)
        'pageNo': 1
    }
    
    saving_response = requests.get(URL, params=params).json()
    
    return deposit_response, saving_response


def api_call_all_pages():
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    api_key = os.getenv("API_KEY")
    topFinGrpNo = '020000'

    deposit_all = []
    page = 1
    while True:
        params = {
            'auth': api_key,
            'topFinGrpNo': topFinGrpNo,
            'pageNo': page
        }
        response = requests.get(BASE_URL + 'depositProductsSearch.json', params=params).json()
        base_list = response.get('result', {}).get('baseList', [])
        if not base_list:
            break
        deposit_all.extend(base_list)
        page += 1

    saving_all = []
    page = 1
    while True:
        params = {
            'auth': api_key,
            'topFinGrpNo': topFinGrpNo,
            'pageNo': page
        }
        response = requests.get(BASE_URL + 'savingProductsSearch.json', params=params).json()
        base_list = response.get('result', {}).get('baseList', [])
        if not base_list:
            break
        saving_all.extend(base_list)
        page += 1

    return deposit_all, saving_all