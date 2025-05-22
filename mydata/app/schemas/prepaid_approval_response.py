from pydantic import BaseModel
from typing import List, Optional
from app.schemas.prepaid_approval import PrepaidApprovalSchema

class PrepaidApprovalResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    approved_cnt: int
    approved_list: List[PrepaidApprovalSchema]
    next_page: Optional[str] = None
