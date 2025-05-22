from pydantic import BaseModel
from typing import List, Optional
from app.schemas.card_bill import CardBillSchema

class CardBillListResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    bill_cnt: int
    bill_list: List[CardBillSchema]
    next_page: Optional[str] = None
