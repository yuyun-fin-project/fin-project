import requests
import os
from dotenv import load_dotenv
import urllib.parse
from requests.exceptions import SSLError
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

# .env 파일 로드
load_dotenv()

def spot_api(start_date, end_date):
    start_dates = datetime.strptime(start_date, "%Y%m%d")  # "20240501" 이런 형식
    end_dates = datetime.strptime(end_date, "%Y%m%d")
    
    date_diff = (end_dates - start_dates).days
    
    base_url = "http://apis.data.go.kr/1160100/service/GetGeneralProductInfoService"
    api_key = os.getenv('SPOT_API')
    endpoints = [
        {
            'url': f"{base_url}/getGoldPriceInfo",
            'params': {
                'serviceKey': api_key,
                'pageNo': '1',
                'numOfRows': 2*date_diff,
                'resultType': 'json',
                'beginBasDt': start_date,
                'endBasDt': end_date,
            }
        },
        {
            'url': f"{base_url}/getOilPriceInfo",
            'params': {
                'serviceKey': api_key,
                'pageNo': '1',
                'numOfRows': 3*date_diff,
                'resultType': 'json',
                'beginBasDt': start_date,
                'endBasDt': end_date,
            }
        },
        {
            'url': f"{base_url}/getCertifiedEmissionReductionPriceInfo",
            'params': {
                'serviceKey': api_key,
                'pageNo': '1',
                'numOfRows': 1*date_diff,
                'resultType': 'json',
                'beginBasDt': start_date,
                'endBasDt': end_date,
                'itmsNm': "KAU24",
            }
        }
    ]
    
    responses = []
    
    for endpoint in endpoints:
        headers = {
            "User-Agent": "curl/8.7.1",
            "Accept": "*/*"
        }
            
        response = requests.get(
        endpoint['url'], 
            params=endpoint['params'],
            headers=headers,
        )
        responses.append(response)

    return responses
