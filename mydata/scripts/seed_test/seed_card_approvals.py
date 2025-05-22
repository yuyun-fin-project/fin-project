# scripts/seed_card_approvals.py

from app.core.database import SessionLocal
from app.models.card_approval import CardApproval
from datetime import datetime
import random

db = SessionLocal()

sample_merchants = ["스타벅스", "GS25", "배달의민족", "쿠팡", "이마트"]
sample_card_ids = ["C123", "C456", "C789"]
org_code = "HANA"

try:
    for _ in range(10):
        record = CardApproval(
            org_code=org_code,
            card_id=random.choice(sample_card_ids),
            approved_dtime=datetime.now(),
            merchant_name=random.choice(sample_merchants),
            approved_amount=round(random.uniform(1000, 50000), 2),
            currency_code="KRW"
        )
        db.add(record)
    db.commit()
    print("✅ 더미 데이터 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)
finally:
    db.close()
