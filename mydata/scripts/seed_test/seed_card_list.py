from app.core.database import SessionLocal
from app.models.card_list import Card

db = SessionLocal()

sample_cards = [
    Card(
        card_id="CARD_001",
        user_id="user123",
        card_num="1234********5678",
        is_consent=True,
        card_name="삼성카드 taptap O",
        card_member="1",
        card_type="01",
        org_code="HANA"
    ),
    Card(
        card_id="CARD_002",
        user_id="user123",
        card_num="5678********1234",
        is_consent=True,
        card_name="국민카드 Simple",
        card_member="1",
        card_type="02",
        org_code="KB"
    )
]

try:
    for card in sample_cards:
        db.add(card)
    db.commit()
    print("✅ 카드 목록 더미 데이터 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러 발생:", e)
finally:
    db.close()
