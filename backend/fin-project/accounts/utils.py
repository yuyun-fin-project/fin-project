from dotenv import load_dotenv
import os
import requests

# .env 파일 로드하기
load_dotenv()

# access 토큰 받는 함수
def get_access_token(code):
    print(os.getenv("GOOGLE_CLIENT_SECRET"))
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": "http://127.0.0.1:8000/accounts/google/callback/",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token


def get_user_info(access_token):
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    userinfo_response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    userinfo = userinfo_response.json()
    
    email = userinfo.get("email")
    name = userinfo.get("name")
    if not email:
        return redirect("/")
    
    return email, name
