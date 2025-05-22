from pydantic import BaseModel
from typing import Optional

class PrepaidApprovalSchema(BaseModel):
    approved_num: str
    user_id: str
    approved_dtime: str
    status: str
    pay_type: str
    merchant_name: Optional[str]
    merchant_regno: Optional[str]
    approved_amt: float

class Config:
    from_attributes = True
