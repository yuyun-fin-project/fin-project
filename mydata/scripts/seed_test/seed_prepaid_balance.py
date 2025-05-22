from app.core.database import SessionLocal
from app.models.prepaid_balance import PrepaidBalance

db = SessionLocal()

sample_balances = [
    PrepaidBalance(
        pp_id="PP123",
        user_id="user123",
        search_timestamp="20240301120000",
        total_balance_amt=35600,
        charge_balance_amt=30000,
        reserve_balance_amt=5600,
        reserve_due_amt=1000,
        exp_due_amt=500
    )
]

try:
    for b in sample_balances:
        db.add(b)
    db.commit()
    print("✅ 선불카드 잔액 더미 데이터 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)
finally:
    db.close()
