from pydantic import BaseModel
from typing import List
from app.schemas.loan_short_term import LoanShortTermSchema

class LoanShortTermListResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    search_timestamp: str
    short_term_cnt: int
    short_term_list: List[LoanShortTermSchema]
