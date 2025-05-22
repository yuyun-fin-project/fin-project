from pydantic import BaseModel
from app.schemas.prepaid_balance import PrepaidBalanceSchema

class PrepaidBalanceResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    search_timestamp: str
    total_balance_amt: float
    charge_balance_amt: float = 0
    reserve_balance_amt: float = 0
    reserve_due_amt: float = 0
    exp_due_amt: float
