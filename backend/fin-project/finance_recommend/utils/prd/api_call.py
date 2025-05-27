import requests
from dotenv import load_dotenv
import os
from django.conf import settings
from rest_framework.decorators import api_view
from pprint import pprint

load_dotenv()

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
deposit_responses = []
saving_responses = []

def api_call():
    i = 1
    for topFinGrpNo in ['020000', '030200', '030300','050000', '060000']:
        max_page = 10
        while i < max_page:
            URL = BASE_URL + 'depositProductsSearch.json'
            params = {
                'auth': os.getenv("API_KEY"),           # .env 파일에 API_KEY 설정 필요
                'topFinGrpNo': topFinGrpNo,            # 금융회사 코드 (은행)
                'pageNo': i
            }
            deposit_response = requests.get(URL, params=params).json()

            deposit_responses.append(deposit_response)
            max_page = deposit_response.get("result", {}).get("max_page_no", 1)
            i += 1
    
    # print(deposit_responses)
    i = 1
    for topFinGrpNo in ['020000', '030200', '030300','050000', '060000']:
        max_page = 10
        while i < max_page:
            URL = BASE_URL + 'savingProductsSearch.json'
            params = {
                'auth': os.getenv("API_KEY"),           # .env 파일에 API_KEY 설정 필요
                'topFinGrpNo': topFinGrpNo,            # 금융회사 코드 (은행)
                'pageNo': i
            }
            saving_response = requests.get(URL, params=params).json()
            saving_responses.append(saving_response)
            max_page = saving_response.get("result", {}).get("max_page_no", 1)
            i += 1
    return deposit_responses, saving_responses

