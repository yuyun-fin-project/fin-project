from pydantic import BaseModel
from typing import Optional

class PrepaidBalanceSchema(BaseModel):
    pp_id: str
    user_id: str
    search_timestamp: Optional[str]
    total_balance_amt: float
    charge_balance_amt: Optional[float]
    reserve_balance_amt: Optional[float]
    reserve_due_amt: Optional[float]
    exp_due_amt: float

class Config:
    from_attributes = True
