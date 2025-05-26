import requests
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse
from datetime import datetime

BASE_URL = 'http://127.0.0.1:8080'
# BASE_URL = 'http://13.125.217.104/'

def get_card_list(request):
    URL = BASE_URL + '/generate/'
    
    data = {
        'username' : request.data.get('username'),
        'useremail' : request.data.get('useremail'),
    }
    
    try:
        # API 요청 보내기
        response = requests.post(URL, json=data)
        
        # 디버깅을 위한 로그 추가
        print(f"응답 상태 코드: {response.status_code}")
        # 응답 상태 코드 확인
        response.raise_for_status()
        
        # 응답이 비어있지 않은지 확인
        if response.text.strip():
            # 응답이 JSON인지 확인 후 파싱
            response_data = response.json()
            return response_data
        else:
            # 빈 응답 처리
            return {"message": "API 응답이 비어 있습니다."}
            
    except requests.exceptions.JSONDecodeError as e:
        # JSON 파싱 오류 처리
        error_msg = f"API 응답이 JSON 형식이 아닙니다: {str(e)}"
        print(error_msg)
        print(f"받은 응답: {response.text[:500]}")
        return {"error": error_msg, "response_text": response.text[:500]}
        
    except requests.exceptions.RequestException as e:
        # 네트워크 또는 HTTP 오류 처리
        error_msg = f"API 요청 오류: {str(e)}"
        print(error_msg)
        return JsonResponse({"error": error_msg}, status=500)
        
    except Exception as e:
        # 기타 예외 처리
        error_msg = f"예상치 못한 오류: {type(e).__name__}: {str(e)}"
        print(error_msg)
        return JsonResponse({"error": error_msg}, status=500)


def get_card_approval(jwt_token, card_id):
    URL = BASE_URL + f'/v1/card/cards/{card_id}/approval-domestic'
    params = {
        'from_date': '20250101',
        'to_date': '20250430',
        'limit': 100,
    }
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # API 요청 보내기
        response = requests.get(URL, headers=headers, params=params)
        
        # 디버깅을 위한 로그 추가
        print(f"응답 상태 코드: {response.status_code}")
        
        # 응답 상태 코드 확인
        response.raise_for_status()
        
        # 응답이 비어있지 않은지 확인
        if response.text.strip():
            # 응답이 JSON인지 확인 후 파싱
            response_data = response.json()
            return response_data
        else:
            # 빈 응답 처리
            return {"message": "API 응답이 비어 있습니다."}
            
    except requests.exceptions.JSONDecodeError as e:
        # JSON 파싱 오류 처리
        error_msg = f"API 응답이 JSON 형식이 아닙니다: {str(e)}"
        print(error_msg)
        print(f"받은 응답: {response.text[:500]}")
        return {"error": error_msg, "response_text": response.text[:500]}
        
    except requests.exceptions.RequestException as e:
        # 네트워크 또는 HTTP 오류 처리
        error_msg = f"API 요청 오류: {str(e)}"
        print(error_msg)
        return {"error": error_msg}
        
    except Exception as e:
        # 기타 예외 처리
        error_msg = f"예상치 못한 오류: {type(e).__name__}: {str(e)}"
        print(error_msg)
        return {"error": error_msg}
    
    
def get_bill(jwt_token):
    URL = BASE_URL + f'/v1/card/bills'
    params = {
        'from_month': '202501',
        'to_month': datetime.now().strftime('%Y%m'),
        # 'to_date' : '202505',
        'limit': 100,
    }
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # API 요청 보내기
        response = requests.get(URL, headers=headers, params=params)
        
        # 응답 상태 코드 확인
        response.raise_for_status()
        
        # 응답이 비어있지 않은지 확인
        if response.text.strip():
            # 응답이 JSON인지 확인 후 파싱
            response_data = response.json()
            return response_data
        else:
            # 빈 응답 처리
            return {"message": "API 응답이 비어 있습니다."}
            
    except requests.exceptions.JSONDecodeError as e:
        # JSON 파싱 오류 처리
        error_msg = f"API 응답이 JSON 형식이 아닙니다: {str(e)}"
        print(error_msg)
        print(f"받은 응답: {response.text[:500]}")
        return {"error": error_msg, "response_text": response.text[:500]}
        
    except requests.exceptions.RequestException as e:
        # 네트워크 또는 HTTP 오류 처리
        error_msg = f"API 요청 오류: {str(e)}"
        print(error_msg)
        return {"error": error_msg}
        
    except Exception as e:
        # 기타 예외 처리
        error_msg = f"예상치 못한 오류: {type(e).__name__}: {str(e)}"
        print(error_msg)
        return {"error": error_msg}