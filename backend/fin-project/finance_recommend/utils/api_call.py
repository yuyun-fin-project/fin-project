import requests
from dotenv import load_dotenv
import os
from django.conf import settings
from rest_framework.decorators import api_view

load_dotenv()

BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

def api_call(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': os.getenv("API_KEY"),           # .env 파일에 API_KEY 설정 필요
        'topFinGrpNo': '020000',            # 금융회사 코드 (은행)
        'pageNo': 1
    }
    
    response = requests.get(URL, params=params).json()
    return response
    # return {}
