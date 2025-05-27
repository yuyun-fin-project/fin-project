from app.core.database import SessionLocal
from app.models.card_bill import CardBill

db = SessionLocal()

sample_bills = [
    CardBill(
        id="BILL_001",
        user_id="user123",
        charge_amt=450000,
        charge_day="15",
        charge_month="202402",
        paid_out_date="20240315"
    ),
    CardBill(
        id="BILL_002",
        user_id="user123",
        charge_amt=312000,
        charge_day="10",
        charge_month="202403",
        paid_out_date="20240410"
    )
]

try:
    for bill in sample_bills:
        db.add(bill)
    db.commit()
    print("✅ 카드 청구 더미 데이터 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)
finally:
    db.close()
