from dotenv import load_dotenv
from django.shortcuts import redirect
import os
import requests
import random
import json

# .env 파일 로드하기
load_dotenv()

# 랜덤 닉네임 생성기
list1 = ['0_', '1_', '2_', '3_', '4_', '5_', '6_', '7_', '8_', '9_']
list2 = [
    "도전적인", "노란색의", "바보같은", "내일의", "감동받은",
    "피곤한", "욕심쟁이", "자신감있는", "방금일어난", "침착한",
    "화가난", "사랑스러운", "의욕없는", "카리스마있는", "낙천적인",
    "비관적인", "초조한", "열정적인", "정신없는", "불안한",
    "귀찮은", "기분좋은", "상상력풍부한", "허세부리는", "찡그린",
    "은은한", "무서운", "졸린", "능글맞은", "엉뚱한",
    "과몰입한", "천진난만한", "시크한", "눈치없는", "귀여운",
    "거만한", "겸손한", "소심한", "단호한", "재빠른",
    "느긋한", "헷갈리는", "화려한", "지친", "엉망진창인",
    "초긍정적인", "불타오르는", "찜찜한", "뻔뻔한", "덜익은"
]
list3 = [
    "MZ세대", "개구쟁이", "한국인", "미국인", "일본인",
    "중국인", "우수교육생", "택시기사", "이세계", "아이돌",
    "백억부자", "천억부자", "천조부자", "천경부자", "천해부자",
    "항하사부자", "아승기부자", "초딩", "중딩", "고딩",
    "취준생", "인싸", "아싸", "프로불참러", "슬랙커",
    "열정러", "스티브잡스빠", "덕후", "찐따", "유튜버",
    "인스타그래머", "틱톡커", "자낳괴", "세무사", "개발자",
    "디자이너", "기획자", "컨설턴트", "사장님", "대장장이",
    "워킹맘", "육아대디", "철학자", "방랑자", "히키코모리",
    "교수님", "교생쌤", "꼰대", "요즘것", "투자자"
]
list4 = [
    "일론머스크", "제프베조스", "워렌버핏", "빌게이츠", "래리페이지",
    "세르게이브린", "마크저커버그", "스티브발머", "래리엘리슨", "버나드아르노",
    "카를로슬림", "마이클블룸버그", "마이클델", "젠슨황", "무케시암바니",
    "프랑수아베당쿠르", "짐월턴", "롭월턴", "앨리스월턴", "장중머우",
    "마화텅", "레이쥔", "리샤오룽", "리자청", "이재용",
    "정용진", "정몽구", "정의선", "최태원", "구광모",
    "조원태", "김범수", "김정주", "서정진", "방시혁",
    "이부진", "이서현", "김택진", "이재현", "이해욱",
    "이웅열", "이상혁", "허창수", "허태수", "이장우",
    "워뇨띠", "손정의", "리사수", "매켄지스콧", "오프라윈프리"
]

USED_FILE = "used_nicknames.json"

def load_used_nicknames():
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_used_nicknames(used):
    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(used), f, ensure_ascii=False)

used_nicknames = load_used_nicknames()

def random_nickname():
    max_combinations = len(list1) * len(list2) * len(list3) * len(list4)
    if len(used_nicknames) >= max_combinations:
        raise ValueError("모든 닉네임 조합이 소진되었습니다.")
    
    while True:
        nickname = f"{random.choice(list1)} {random.choice(list2)} {random.choice(list3)} {random.choice(list4)}"
        if nickname not in used_nicknames:
            used_nicknames.add(nickname)
            save_used_nicknames(used_nicknames)
            return nickname
        
# access 토큰 받는 함수
def get_access_token(code):
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
    load_used_nicknames()
    email = userinfo.get("email")
    name = userinfo.get("name")
    nickname = random_nickname()
    if not email:
        return redirect("/")
    
    return email, name, nickname


def get_kakao_user_info(access_token):
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_info_url, headers=headers)
    user_info = user_response.json()
    kakao_id = user_info.get("id")
    kakao_account = user_info.get("kakao_account", {})
    email = kakao_account.get("email", f"{kakao_id}@kakao.com")
    name = kakao_account.get("profile", {}).get("nickname", "kakao_user")
    nickname = random_nickname()
    
    return email, name, nickname