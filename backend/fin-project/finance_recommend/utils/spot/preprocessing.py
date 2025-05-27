from datetime import datetime
from django.db import transaction
from finance_recommend.models import Gold, Oil, Carbon  
import re
from pprint import pprint

def camel_to_snake(name):
    # 대문자 앞에 _를 넣고 소문자로 변환
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()
"""
{'response':
 {'body':
  {'items':
   {'item':
    [{'basDt': '20250522',
    'clpr': '148100',
    'fltRt': '.09',
    'hipr': '148700',
    'isinCd': 'KRD040200002',
    'itmsNm': '금 99.99_1Kg',
    'lopr': '147010',
    'mkp': '147390',
    'srtnCd': '04020000',
    'trPrc': '21058218970',
    'trqu': '142248',
    'vs': '140'},
    ]}
    }
}
"""
    
# 금융 데이터 전처리 프로세스
def data_preprocessing(data, spot_type, spot_name):
    # 금융 상품 전처리
    spot_field_names = [field.name for field in spot_type._meta.fields]
    cleaned_spot_list = []
    # 상품 리스트 추출
    spot_list = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
    for spot in spot_list:
        spot_temp = {}
        for key, value in spot.items():
            if camel_to_snake(key) in spot_field_names:
                spot_temp[key] = value
        spot_temp["spot_type"] = spot_name
        cleaned_spot_list.append(spot_temp)
    return cleaned_spot_list
