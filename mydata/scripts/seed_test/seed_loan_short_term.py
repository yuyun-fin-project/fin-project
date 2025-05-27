from app.core.database import SessionLocal
from app.models.loan_short_term import LoanShortTerm

db = SessionLocal()

loans = [
    LoanShortTerm(
        id="ST001",
        user_id="user123",
        org_code="HANA",
        search_timestamp="20240517170000",
        loan_dtime="20240515100000",
        loan_amt=500000,
        balance_amt=420000,
        pay_due_date="20240615",
        int_rate=14.2
    )
]

try:
    for row in loans:
        db.add(row)
    db.commit()
    print("✅ 단기대출 더미 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()
