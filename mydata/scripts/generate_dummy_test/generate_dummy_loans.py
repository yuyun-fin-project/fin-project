from app.core.database import SessionLocal
from app.models.user import User
from app.models.loan_short_term import LoanShortTerm
from app.models.loan_long_term import LoanLongTerm
from faker import Faker
import uuid
import random
from datetime import datetime, timedelta

db = SessionLocal()
fake = Faker()
Faker.seed(88)

try:
    users = db.query(User).all()
    short_term_loans = []
    long_term_loans = []

    for user in users:
        # 단기대출: 0~2건
        for _ in range(random.randint(0, 2)):
            dt = fake.date_between(start_date="-3M", end_date="today")
            short_term_loans.append(LoanShortTerm(
                id=str(uuid.uuid4()),
                user_id=user.id,
                org_code=random.choice(["HANA", "KB", "SAMSUNG"]),
                search_timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
                loan_dtime=dt.strftime("%Y%m%d%H%M%S"),
                loan_amt=random.randint(100000, 1000000),
                balance_amt=random.randint(10000, 800000),
                pay_due_date=(dt + timedelta(days=30)).strftime("%Y%m%d"),
                int_rate=round(random.uniform(10.0, 19.9), 1)
            ))

        # 장기대출: 0~1건
        if random.random() < 0.4:
            dt = fake.date_between(start_date="-12M", end_date="-1M")
            long_term_loans.append(LoanLongTerm(
                id=str(uuid.uuid4()),
                user_id=user.id,
                org_code=random.choice(["HANA", "KB", "SAMSUNG"]),
                search_timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
                loan_num=f"LN{random.randint(1000, 9999)}",
                loan_dtime=dt.strftime("%Y%m%d"),
                loan_type=random.choice(["신용대출", "카드론"]),
                loan_name=random.choice(["마이핏론", "하나신용플랜"]),
                loan_amt=random.randint(3000000, 20000000),
                int_rate=round(random.uniform(5.0, 14.0), 2),
                exp_date=(dt + timedelta(days=365 * 2)).strftime("%Y%m%d"),
                balance_amt=random.randint(1000000, 15000000),
                repay_method=random.choice(["01", "02"]),
                int_amt=random.randint(10000, 300000)
            ))

    db.add_all(short_term_loans + long_term_loans)
    db.commit()
    print(f"✅ 단기대출 {len(short_term_loans)}건, 장기대출 {len(long_term_loans)}건 생성 완료")

except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()
