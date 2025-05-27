from app.core.database import SessionLocal
from app.models.prepaid_approval import PrepaidApproval

db = SessionLocal()

sample_approvals = [
    PrepaidApproval(
        approved_num="PPA001",
        user_id="user123",
        approved_dtime="202405151030",
        status="01",
        pay_type="02",
        merchant_name="CU 서울역점",
        merchant_regno="789-12-34567",
        approved_amt=8000
    ),
    PrepaidApproval(
        approved_num="PPA002",
        user_id="user123",
        approved_dtime="202405151140",
        status="01",
        pay_type="02",
        merchant_name="배달의민족",
        merchant_regno="111-22-33333",
        approved_amt=15000
    )
]

try:
    for a in sample_approvals:
        db.add(a)
    db.commit()
    print("✅ 선불 승인내역 더미 데이터 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)
finally:
    db.close()
