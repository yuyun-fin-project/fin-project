from app.core.database import Base, engine
from app.models import (
    user, card_list, card_bill, card_approval_domestic,
    prepaid_balance, prepaid_approval, point,
    loan_short_term, loan_long_term
)

Base.metadata.drop_all(bind=engine)   # 🔥 테이블 전부 삭제
Base.metadata.create_all(bind=engine) # 🔥 테이블 전부 재생성
print("✅ 모든 테이블 삭제 후 재생성 완료")
