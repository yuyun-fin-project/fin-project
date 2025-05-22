from sqlalchemy import Column, String, Integer, Float
from app.core.database import Base
import uuid

class CardBill(Base):
    __tablename__ = "card_bills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # ✅ 수정
    user_id = Column(String, index=True, nullable=False)
    charge_amt = Column(Float, nullable=False)
    charge_day = Column(String, nullable=False)  # "15"
    charge_month = Column(String, nullable=False)  # "202402"
    paid_out_date = Column(String, nullable=False)  # "20240315"
    org_code = Column(String, nullable=False)
