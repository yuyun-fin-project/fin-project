# app/schemas/card_bill_request.py

from pydantic import BaseModel, Field
from typing import Optional

class CardBillRequest(BaseModel):
    from_month: str = Field(..., pattern=r"^\d{6}$", description="시작 년월 (YYYYMM)")
    to_month: str = Field(..., pattern=r"^\d{6}$", description="종료 년월 (YYYYMM)")
    next_page: Optional[str] = Field(None, description="다음 페이지 기준 청구월")
    limit: int = Field(..., ge=1, le=100, description="최대 조회 개수")
