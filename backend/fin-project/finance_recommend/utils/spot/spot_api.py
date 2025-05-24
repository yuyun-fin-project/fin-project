import requests
import os
from dotenv import load_dotenv
import urllib.parse

# .env 파일 로드
load_dotenv()

def spot_api(request):
    SPOT_API = os.getenv("SPOT_API")
    BASE_URL = "https://apis.data.go.kr/1160100/service/GetGeneralProductInfoService"
    spot_url = BASE_URL + "getGoldPriceInfo"
    spot_url += urllib.parse.urlencode({
            "serviceKey": SPOT_API,
            "type": "json",
            "numOfRows": 1,
            "pageNo": 1,
            "resultType": "json",
        })
    response = requests.get(spot_url).json()
    return response