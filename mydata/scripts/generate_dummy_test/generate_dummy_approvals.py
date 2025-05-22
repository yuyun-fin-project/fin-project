from app.core.database import SessionLocal
from app.models.card_list import Card
from app.models.card_approval_domestic import CardApprovalDomestic
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

db = SessionLocal()
fake = Faker()
Faker.seed(99)

try:
    cards = db.query(Card).all()
    approvals = []

    for card in cards:
        for _ in range(random.randint(10, 20)):
            approved_dtime = fake.date_time_between(start_date="-4M", end_date="now")
            approvals.append(CardApprovalDomestic(
                id=str(uuid.uuid4()),
                user_id=card.user_id,
                card_id=card.card_id,
                approved_dtime=approved_dtime.strftime("%Y%m%d%H%M"),
                approved_num=f"A{fake.unique.random_int(1000, 9999)}",
                status=random.choice(["01", "02"]),  # 승인/취소
                pay_type=random.choice(["01", "02"]),  # 신용/체크
                merchant_name=fake.company() + " " + fake.city(),
                merchant_regno=fake.bothify(text="###-##-#####"),
                approved_amt=random.randint(1000, 100000),
                total_install_cnt=random.choice([None, 2, 3, 6])
            ))

    db.add_all(approvals)
    db.commit()
    print(f"✅ 승인내역 {len(approvals)}건 생성 완료")

except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()
