import requests
import os
from dotenv import load_dotenv
import urllib.parse
from requests.exceptions import SSLError
from rest_framework.response import Response
from rest_framework import status

# .env 파일 로드
load_dotenv()

def spot_api(start_date, end_date):
    base_url = "http://apis.data.go.kr/1160100/service/GetGeneralProductInfoService"
    api_key = os.getenv('SPOT_API')
    endpoints = [
        {
            'url': f"{base_url}/getGoldPriceInfo",
            'params': {
                'serviceKey': api_key,
                'pageNo': '1',
                'numOfRows': '31',
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
                'numOfRows': '31',
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
                'numOfRows': '31',
                'resultType': 'json',
                'beginBasDt': start_date,
                'endBasDt': end_date
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
