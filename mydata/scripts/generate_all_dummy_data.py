# # scripts/generate_all_dummy_data.py

# from app.core.database import SessionLocal
# from app.models.user import User
# from app.models.card_list import Card
# from app.models.card_bill import CardBill
# from app.models.card_approval_domestic import CardApprovalDomestic
# from app.models.point import Point
# from app.models.prepaid_balance import PrepaidBalance
# from app.models.prepaid_approval import PrepaidApproval
# from app.models.loan_short_term import LoanShortTerm
# from app.models.loan_long_term import LoanLongTerm
# from app.core.security import hash_password 

# import uuid
# from faker import Faker
# from datetime import datetime, timedelta
# import random


# fake = Faker('ko_KR')
# Faker.seed(777)
# db = SessionLocal()

# ORG_CODES = {
# "POST": "우체국",
# "KB_CARD": "KB국민카드",
# "WOORI_CARD": "우리카드",
# "SC": "SC은행",
# "NONGHYUP": "농협은행",
# "HANA_CARD": "하나카드",
# "LOTTE": "롯데카드",
# "WOORI": "우리은행",
# "KB_BANK": "국민은행",
# "IBK": "IBK기업은행",
# "SHINHAN_BANK": "신한은행",
# "HANA_BANK": "하나은행",
# "SAMSUNG": "삼성카드",
# "SHINHAN_CARD": "신한카드",
# "HYUNDAI": "현대카드",
# "BC": "비씨카드",
# "MIRAE": "미래에셋생명",
# "KAKAO": "카카오뱅크"
# }

# try:
#     # 1. 사용자 생성
#     print("👥 사용자 생성 중...")
#     users = []
#     for _ in range(100):
#         name = fake.name()
#         users.append(User(
#             id=str(uuid.uuid4()),
#             username=name,
#             email=fake.unique.email(),
#             hashed_password=hash_password("test1234")  # 모든 유저 비밀번호는 동일하게
#         ))
#     db.add_all(users)
#     db.commit()

#     # 2. 카드 + 청구
#     print("💳 카드 및 청구 정보 생성 중...")
#     cards = []
#     bills = []
#     for user in users:
#         for _ in range(random.randint(1, 7)):
#             card_id = f"CARD_{uuid.uuid4().hex[:8]}"
#             org_code = random.choice(list(ORG_CODES.keys()))
#             cards.append(Card(
#                 user_id=user.id,
#                 card_id=card_id,
#                 card_name=fake.credit_card_provider(),
#                 card_num=fake.credit_card_number(),
#                 is_consent=True,
#                 card_member="1",
#                 card_type=random.choice(["01", "02"]),
#                 org_code=org_code
#             ))

#             for _ in range(random.randint(3, 6)):
#                 bills.append(CardBill(
#                     user_id=user.id,
#                     org_code=org_code,
#                     charge_amt=random.randint(100000, 1000000),
#                     charge_day=str(random.choice([5, 10, 15, 25])),
#                     charge_month=fake.date_between(start_date="-6M", end_date="today").strftime("%Y%m"),
#                     paid_out_date=fake.date_between(start_date="today", end_date="+30d").strftime("%Y%m%d")
#                 ))

#     db.add_all(cards + bills)
#     db.commit()

#     # 3. 카드 승인내역
#     print("🧾 카드 승인내역 생성 중...")
#     approvals = []
#     for card in cards:
#         for _ in range(random.randint(5, 15)):
#             approved_time = fake.date_time_between(start_date="-4M", end_date="now")
#             approvals.append(CardApprovalDomestic(
#                 user_id=card.user_id,
#                 card_id=card.card_id,
#                 approved_dtime=approved_time.strftime("%Y%m%d%H%M"),
#                 approved_num=f"A{uuid.uuid4().hex[:8]}",
#                 status=random.choice(["01", "02"]),
#                 pay_type=random.choice(["01", "02"]),
#                 merchant_name=fake.company() + " " + fake.city(),
#                 merchant_regno=fake.bothify(text="###-##-#####"),
#                 approved_amt=random.randint(1000, 500000),
#                 total_install_cnt=random.choice([None, 2, 3, 6])
#             ))
#     db.add_all(approvals)
#     db.commit()

# scripts/generate_all_dummy_data.py

from app.core.database import SessionLocal
from app.models.user import User
from app.models.card_list import Card
from app.models.card_bill import CardBill
from app.models.card_approval_domestic import CardApprovalDomestic
from app.models.point import Point
from app.models.prepaid_balance import PrepaidBalance
from app.models.prepaid_approval import PrepaidApproval
from app.models.loan_short_term import LoanShortTerm
from app.models.loan_long_term import LoanLongTerm
from app.core.security import hash_password 
from scripts.dummy_category import CARDS_LIST

import uuid
from faker import Faker
from datetime import datetime, timedelta
import random


fake = Faker('ko_KR')
Faker.seed()
db = SessionLocal()

ORG_CODES = {
"KB_CARD": "KB국민카드",
"WOORI_CARD": "우리카드",
"HANA_CARD": "하나카드",
"LOTTE": "롯데카드",
"IBK": "IBK기업은행",
"SAMSUNG": "삼성카드",
"SHINHAN_CARD": "신한카드",
"HYUNDAI": "현대카드",
"BC": "BC 바로카드",
"NH": "NH농협카드",
}

# 소비 카테고리 - 소비처 목록 정의
SPENDING_CATEGORIES = {
    "식비": {
        "식당/카페": ["스타벅스", "투썸플레이스", "이디야", "맥도날드", "롯데리아", "버거킹", "서브웨이", "본죽", "김밥천국", "CU", "GS25", "세븐일레븐"],
        "배달": ["배달의민족", "요기요", "쿠팡이츠", "배달통"]
    },
    "교통": {
        "대중교통": ["서울교통공사", "코레일", "버스", "택시"],
        "차량": ["SK에너지", "GS칼텍스", "현대오일뱅크", "S-OIL", "쏘카", "그린카", "타다"]
    },
    "쇼핑": {
        "온라인": ["쿠팡", "11번가", "G마켓", "옥션", "위메프", "티몬", "네이버쇼핑", "SSG닷컴"],
        "오프라인": ["이마트", "홈플러스", "롯데마트", "다이소", "올리브영", "롭스"]
    },
    "주거/관리비": {
        "월세/관리비": ["월세", "관리비", "전기요금", "수도요금", "가스요금"],
        "인터넷/통신": ["SK브로드밴드", "KT", "LG유플러스", "SKT", "KT", "LG U+"]
    },
    "의료/건강": {
        "병원": ["내과", "치과", "안과", "피부과", "이비인후과", "정형외과"],
        "약국/건강관리": ["약국", "헬스장", "필라테스", "요가"]
    },
    "문화/여가": {
        "엔터테인먼트": ["CGV", "메가박스", "롯데시네마", "넷플릭스", "왓챠", "디즈니플러스", "멜론", "지니뮤직"],
        "취미/여행": ["교보문고", "YES24", "알라딘", "여행사", "호텔", "숙박"]
    },
    "교육": {
        "학원/강의": ["영어학원", "학원비", "온라인강의", "인프런", "클래스101"],
        "도서/자료": ["교보문고", "알라딘", "반디앤루니스"]
    },
    "기타": {
        "기부/선물": ["기부금", "선물", "경조사비"],
        "미용/뷰티": ["미용실", "네일샵", "왁싱", "마사지"]
    }
}

# 모든 소비처 목록을 하나의 리스트로 통합
ALL_MERCHANTS = []
for category, subcategories in SPENDING_CATEGORIES.items():
    for subcategory, merchants in subcategories.items():
        for merchant in merchants:
            ALL_MERCHANTS.append((category, subcategory, merchant))

try:
    # 1. 사용자 생성
    print("👥 사용자 생성 중...")
    users = []
    for _ in range(100):
        name = fake.name()
        users.append(User(
            id=str(uuid.uuid4()),
            username=name,
            email=fake.unique.email(),
            hashed_password=hash_password("test1234")  # 모든 유저 비밀번호는 동일하게
        ))
    db.add_all(users)
    db.commit()

    # 2. 카드 + 청구
    print("💳 카드 및 청구 정보 생성 중...")
    cards = []
    bills = []
    for user in users:
        for _ in range(random.randint(1, 7)):
            card_id = f"CARD_{uuid.uuid4().hex[:8]}"
            org_code = random.choice(list(ORG_CODES.keys()))
            if ORG_CODES[org_code] in CARDS_LIST.keys():
                fake_card_name = random.choice(list(CARDS_LIST[ORG_CODES[org_code]]))
            else:
                fake_card_name = fake.credit_card_provider()
            cards.append(Card(
                user_id=user.id,
                card_id=card_id,
                card_name= fake_card_name,
                card_num=fake.credit_card_number(),
                is_consent=True,
                card_member="1",
                card_type=random.choice(["01", "02", "03"]),
                org_code=org_code
            ))

            for _ in range(random.randint(3, 6)):
                bills.append(CardBill(
                    user_id=user.id,
                    org_code=org_code,
                    charge_amt=random.randint(100000, 1000000),
                    charge_day=str(charge_day := random.choice([5, 10, 15, 25])),
                    charge_month=(charge_date := fake.date_between(start_date="-6M", end_date="today")).strftime("%Y%m"),
                    paid_out_date=(
                        datetime(charge_date.year, charge_date.month + 1, int(charge_day))
                        if charge_date.month < 12
                        else datetime(charge_date.year + 1, 1, int(charge_day))
                    ).strftime("%Y%m%d")
                ))

    db.add_all(cards + bills)
    db.commit()

    # 3. 카드 승인내역
    print("🧾 카드 승인내역 생성 중...")
    approvals = []
    for card in cards:
        for _ in range(random.randint(5, 15)):
            # 카테고리, 서브 카테고리, 소비처를 랜덤하게 선택
            category, subcategory, merchant = random.choice(ALL_MERCHANTS)
            
            # 카테고리별 금액 범위 설정
            amount_ranges = {
                "식비": (5000, 50000),
                "교통": (1200, 30000),
                "쇼핑": (10000, 500000),
                "주거/관리비": (30000, 300000),
                "의료/건강": (5000, 100000),
                "문화/여가": (8000, 150000),
                "교육": (30000, 300000),
                "기타": (10000, 200000)
            }
            
            min_amount, max_amount = amount_ranges.get(category, (1000, 500000))
            if card.card_type == "01":
                pay_type = "01"
            elif card.card_type == "02":
                pay_type = "02"
            else:
                pay_type = random.choice(["01", "02"]),
            # 카테고리별 할부 여부 설정 (쇼핑, 의료/건강, 문화/여가, 교육은 할부 가능성 높임)
            if category in ["쇼핑", "의료/건강", "문화/여가", "교육"] and random.random() < 0.3:
                installment = random.choice([2, 3, 6, 12])
            else:
                installment = None
            
            approved_time = fake.date_time_between(start_date="-4M", end_date="now")
            approvals.append(CardApprovalDomestic(
                user_id=card.user_id,
                card_id=card.card_id,
                approved_dtime=approved_time.strftime("%Y%m%d%H%M"),
                approved_num=f"A{uuid.uuid4().hex[:8]}",
                status=random.choice(["01", "02", "03"]),
                # pay_type=random.choice(["01", "02"]),
                pay_type=pay_type,
                merchant_name=merchant,  # 소비처명만 사용
                merchant_regno=fake.bothify(text="###-##-#####"),
                approved_amt=random.randint(min_amount, max_amount),  # 카테고리별 금액 범위 적용
                total_install_cnt=installment
            ))
    db.add_all(approvals)
    db.commit()
    

    # 4. 포인트
    print("⭐ 포인트 정보 생성 중...")
    points = []
    for user in users:
        for org_code in random.sample(list(ORG_CODES.keys()), random.randint(1, 4)):
            points.append(Point(
                id=str(uuid.uuid4()),  # id 필드 추가
                user_id=user.id,
                org_code=org_code,
                search_timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
                point_name=f"{org_code} 포인트",
                remain_point_amt=random.randint(1000, 30000),
                expiring_point_amt=random.randint(0, 5000)
            ))
    db.add_all(points)
    db.commit()

    # 5. 선불카드 잔액 및 승인
    print("💰 선불카드 잔액 및 승인내역 생성 중...")
    prepaid_balances = []
    prepaid_approvals = []
    for user in users:
        for _ in range(random.randint(0, 4)):
            pp_id = f"PP_{uuid.uuid4().hex[:8]}"
            org_code = random.choice(list(ORG_CODES.keys()))
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            prepaid_balances.append(PrepaidBalance(
                user_id=user.id,
                org_code=org_code,
                pp_id=pp_id,
                search_timestamp=timestamp,
                total_balance_amt=random.randint(5000, 50000),
                charge_balance_amt=random.randint(3000, 30000),
                reserve_balance_amt=random.randint(1000, 15000),
                reserve_due_amt=random.randint(0, 3000),
                exp_due_amt=random.randint(0, 2000)
            ))

            for _ in range(random.randint(10, 15)):
                approved_time = fake.date_time_between(start_date="-3M", end_date="now")
                prepaid_approvals.append(PrepaidApproval(
                    user_id=user.id,
                    org_code=org_code,
                    pp_id=pp_id,
                    approved_dtime=approved_time.strftime("%Y%m%d%H%M"),
                    approved_num=f"PP{fake.unique.random_int(1000,9999)}",
                    status=random.choice(["01", "02"]),
                    pay_type=random.choice(["01", "02"]),
                    merchant_name=fake.company() + " " + fake.city(),
                    merchant_regno=fake.bothify(text="###-##-#####"),
                    approved_amt=random.randint(500, 30000)
                ))
    db.add_all(prepaid_balances + prepaid_approvals)
    db.commit()

    # 6. 대출
    print("🏦 단기 및 장기 대출 생성 중...")
    short_loans = []
    long_loans = []
    for user in users:
        if random.choice([True, False]):
            short_loans.append(LoanShortTerm(
                id=str(uuid.uuid4()),  # id 필드 추가
                user_id=user.id,
                org_code=random.choice(list(ORG_CODES.keys())),
                search_timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
                loan_dtime=fake.date_time_between(start_date="-2M", end_date="now").strftime("%Y%m%d%H%M%S"),
                loan_amt=random.randint(100000, 1000000),
                balance_amt=random.randint(10000, 900000),
                pay_due_date=(datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y%m%d"),
                int_rate=round(random.uniform(10.0, 19.9), 1)
            ))

        if random.choice([True, False]):
            long_loans.append(LoanLongTerm(
                id=str(uuid.uuid4()),  # id 필드 추가
                user_id=user.id,
                org_code=random.choice(list(ORG_CODES.keys())),
                search_timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
                loan_num=f"LN{uuid.uuid4().hex[:8]}",
                loan_dtime=fake.date_between(start_date="-1y", end_date="today").strftime("%Y%m%d"),
                loan_type=random.choice(["신용대출", "학자금대출", "주택담보대출"]),
                loan_name=fake.bs().title(),
                loan_amt=random.randint(1000000, 30000000),
                int_rate=round(random.uniform(3.0, 15.0), 1),
                exp_date=(datetime.now() + timedelta(days=random.randint(180, 1080))).strftime("%Y%m%d"),
                balance_amt=random.randint(100000, 25000000),
                repay_method=random.choice(["01", "02"]),
                int_amt=random.randint(50000, 300000)
            ))
    db.add_all(short_loans + long_loans)
    db.commit()

    print("✅ 전체 더미 데이터 생성 완료!")

except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)

finally:
    db.close()
