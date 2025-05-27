# 연동 테스트 코드

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.models.card_approval import CardApproval
# from app.schemas.card_approval import CardApprovalSchema
# from typing import List

# router = APIRouter(
#     prefix="/card",
#     tags=["Card Approvals"]
# )

# @router.get("/approvals", response_model=List[CardApprovalSchema])
# def get_approvals(db: Session = Depends(get_db)):
#     return db.query(CardApproval).all()
