from pydantic import BaseModel
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.card_approval_domestic import CardApprovalDomesticSchema

class CardApprovalDomesticResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    approved_cnt: int
    approved_list: List[CardApprovalDomesticSchema]
    next_page: Optional[str] = None
