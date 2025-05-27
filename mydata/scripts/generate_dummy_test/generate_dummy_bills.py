from app.core.database import SessionLocal
from app.models.card_list import Card
from app.models.card_bill import CardBill
from faker import Faker
import random
from datetime import datetime, timedelta

db = SessionLocal()
fake = Faker()
Faker.seed(42)

try:
    cards = db.query(Card).all()
    bills = []

    for card in cards:
        for _ in range(random.randint(1, 3)):
            base_date = fake.date_between(start_date="-4M", end_date="today")
            charge_month = base_date.strftime("%Y%m")
            paid_out_date = (base_date + timedelta(days=30)).strftime("%Y%m%d")

            bill = CardBill(
                user_id=card.user_id,
                org_code=card.org_code,
                charge_month=charge_month,
                charge_amt=random.randint(10000, 800000),
                charge_day=str(random.choice([5, 10, 15, 25])),
                paid_out_date=paid_out_date
            )
            bills.append(bill)

    db.add_all(bills)
    db.commit()
    print(f"✅ 청구 정보 {len(bills)}건 생성 완료")

except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()
