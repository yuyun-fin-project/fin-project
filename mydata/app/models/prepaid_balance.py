from sqlalchemy import Column, String, Float
from app.core.database import Base
import uuid

class PrepaidBalance(Base):
    __tablename__ = "prepaid_balances"

    user_id = Column(String, index=True, nullable=False)
    search_timestamp = Column(String)    
    total_balance_amt = Column(Float, nullable=False)
    charge_balance_amt = Column(Float)
    reserve_balance_amt = Column(Float)
    reserve_due_amt = Column(Float)
    exp_due_amt = Column(Float)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # ✅ 요거 필요
    org_code = Column(String, nullable=False)
    pp_id = Column(String, nullable=False)

