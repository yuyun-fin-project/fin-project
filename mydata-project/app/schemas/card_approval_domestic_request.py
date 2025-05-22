# app/schemas/card_approval_domestic_request.py

from pydantic import BaseModel, Field
from typing import Optional

class CardApprovalDomesticRequest(BaseModel):
    from_date: str = Field(..., pattern=r"^\d{8}$", description="조회 시작일자 (YYYYMMDD)")
    to_date: str = Field(..., pattern=r"^\d{8}$", description="조회 종료일자 (YYYYMMDD)")
    next_page: Optional[str] = Field(None, description="다음 페이지 기준 승인일시")
    limit: int = Field(..., ge=1, le=100, description="최대 조회 개수")
