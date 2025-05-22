from pydantic import BaseModel
from typing import List
from app.schemas.loan_long_term import LoanLongTermSchema

class LoanLongTermListResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    search_timestamp: str
    long_term_cnt: int
    long_term_list: List[LoanLongTermSchema]
