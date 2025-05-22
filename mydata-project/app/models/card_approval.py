# 연동 테스트코드 : app/models/card_approval.py

# from sqlalchemy import Column, Integer, String, Float, DateTime
# from app.core.database import Base

# class CardApproval(Base):
#     __tablename__ = "card_approvals"

#     id = Column(Integer, primary_key=True, index=True)
#     org_code = Column(String, nullable=False)
#     card_id = Column(String, nullable=False)
#     approved_dtime = Column(DateTime, nullable=False)
#     merchant_name = Column(String)
#     approved_amount = Column(Float, nullable=False)
#     currency_code = Column(String, default="KRW")
