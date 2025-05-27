from sqlalchemy import Column, String, Integer, Float
from app.core.database import Base
import uuid

class CardApprovalDomestic(Base):
    __tablename__ = "card_approvals_domestic"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    card_id = Column(String, nullable=False)
    approved_dtime = Column(String, nullable=False)
    approved_num = Column(String, nullable=False)
    status = Column(String, nullable=False)
    pay_type = Column(String, nullable=False)
    merchant_name = Column(String)
    merchant_regno = Column(String)
    approved_amt = Column(Integer, nullable=False)
    total_install_cnt = Column(Integer)