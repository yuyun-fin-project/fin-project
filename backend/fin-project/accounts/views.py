from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import os
import urllib.parse
from .utils import get_access_token, get_user_info

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
    print(f'User: {user}')
    if created:
        print(f"User created: {user}")
    else:
        print(f"User exists: {user}")
    
    refresh_token = RefreshToken.for_user(user)
    
    redirect_url = f"http://localhost:8000/?access={access_token}"

    response = redirect(redirect_url)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=60*60*24*14
    )
    print(response)
    return response

# refresh 토큰 전달하기
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get('refresh_token')
        return super().post(request, *args, **kwargs)