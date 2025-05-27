'''
응답 리팩토링 스키마
'''

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.card_list import CardSchema

class CardListResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    search_timestamp: str
    card_cnt: int
    card_list: List[CardSchema]
    next_page: Optional[str] = None
