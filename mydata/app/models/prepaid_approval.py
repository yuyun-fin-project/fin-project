from sqlalchemy import Column, String, Float
import uuid
from app.core.database import Base

class PrepaidApproval(Base):
    __tablename__ = "prepaid_approvals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # ✅ 필수!
    user_id = Column(String, nullable=False)
    org_code = Column(String, nullable=False)
    pp_id = Column(String, nullable=False)
    approved_dtime = Column(String, nullable=False)
    approved_num = Column(String, nullable=False)
    status = Column(String, nullable=False)
    pay_type = Column(String, nullable=False)
    merchant_name = Column(String)
    merchant_regno = Column(String)
    approved_amt = Column(Float, nullable=False)