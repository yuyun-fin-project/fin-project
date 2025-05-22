from app.core.database import SessionLocal
from app.models.card_approval_domestic import CardApprovalDomestic

db = SessionLocal()

approvals = [
    CardApprovalDomestic(
        approved_num="A001",
        user_id="user123",
        card_id="CARD_001",  # ← 추가
        approved_dtime="202402151030",
        status="01",
        pay_type="01",
        merchant_name="스타벅스 강남역점",
        merchant_regno="123-45-67890",
        approved_amt=5500,
        total_install_cnt=None
    ),
    CardApprovalDomestic(
        approved_num="A002",
        user_id="user123",
        card_id="CARD_001",  # ← 추가
        approved_dtime="202402161030",
        status="01",
        pay_type="02",
        merchant_name="GS25 서초점",
        merchant_regno="456-78-12345",
        approved_amt=2100,
        total_install_cnt=2
    )
]

try:
    for item in approvals:
        db.add(item)
    db.commit()
    print("✅ 카드 승인내역 더미 데이터 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)
finally:
    db.close()
