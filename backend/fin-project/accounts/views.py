from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
import os
import urllib.parse
import requests
from .utils import get_access_token, get_user_info, get_kakao_user_info

# Create your views here.
# 환경변수 로드
load_dotenv()

# 구글 로그인 요청 보내기
@ api_view(['GET', 'POST'])
def google_login(request):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8000/accounts/google/callback/"
    scope = "openid email profile"
    response_type = "code"

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": scope,
            "prompt": "select_account",
        })
    )

    return redirect(google_auth_url)



def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

# 구글 응답 처리하기
def google_callback(request):
    User = get_user_model()
    
    # Google 에서 준 인가 코드
    code = request.GET.get("code")
    if not code:
        print("No code provided")
        return redirect("/")
    
    # Google에서 엑세스 토큰 요청
    access_token = get_access_token(code)
    
    # 사용자 정보 요청
    email, name, nickname = get_user_info(access_token)
    
    # 사용자 생성 또는 로그인
    user, created = User.objects.get_or_create(
        useremail=email,
        username=name,
        nickname=nickname 
    )
    
    refresh_token = RefreshToken.for_user(user)
    access_token = str(refresh_token.access_token)

    response = redirect(f"http://localhost:5173/login-success?access={access_token}")
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=60 * 60 * 24 * 14
    )
    return response

# refresh 토큰 전달하기
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get('refresh_token')
        return super().post(request, *args, **kwargs)

# 카카오 로그인
@api_view(['GET'])
def kakao_login(request):
    client_id = os.getenv("KAKAO_REST_API_KEY")
    redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
    response_type = "code"

    kakao_auth_url = (
        "https://kauth.kakao.com/oauth/authorize?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "prompt": "select_account",
        })
    )

    return redirect(kakao_auth_url)

@api_view(['GET', 'POST'])
# 카카오 응답 처리하기
def kakao_callback(request):
    code = request.GET.get("code")
    if not code:
        return Response({"error": "No code provided"}, status=400)

    # 1. access token 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("KAKAO_REST_API_KEY"),
        "redirect_uri": os.getenv("KAKAO_REDIRECT_URI"),
        "code": code,
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return Response({"error": "Failed to retrieve access token"}, status=400)

    # 2. 사용자 정보 요청 (utils)
    email, name,nickname = get_kakao_user_info(access_token)

    # 3. 유저 생성 or 로그인 처리
    User = get_user_model()
    
    user, created = User.objects.get_or_create(
        useremail=email,
        username=name,
        nickname=nickname 
    )

    refresh_token = RefreshToken.for_user(user)
    access_token = str(refresh_token.access_token)

    response = redirect(f"http://localhost:5173/login-success?access={access_token}")
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=60 * 60 * 24 * 14
    )
    return response


# 로그아웃
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=205)
    except Exception:
        return Response(status=400)