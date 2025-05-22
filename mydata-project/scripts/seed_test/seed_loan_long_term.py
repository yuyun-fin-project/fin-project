from app.core.database import SessionLocal
from app.models.loan_long_term import LoanLongTerm

db = SessionLocal()

loans = [
    LoanLongTerm(
        id="LT001",
        user_id="user123",
        org_code="HANA",
        search_timestamp="20240517170000",
        loan_num="LN001",
        loan_dtime="20230515",
        loan_type="신용대출",
        loan_name="하나 신용대출",
        loan_amt=10000000,
        int_rate=12.5,
        exp_date="20260515",
        balance_amt=8200000,
        repay_method="01",
        int_amt=104166
    )
]

try:
    for row in loans:
        db.add(row)
    db.commit()
    print("✅ 장기대출 더미 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()
