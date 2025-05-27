# app/schemas/card_list_request.py

from pydantic import BaseModel, Field
from typing import Optional


class CardListRequest(BaseModel):
    org_code: str = Field(..., min_length=2, description="기관 코드 (대문자)")
    search_timestamp: Optional[str] = Field(
        None, pattern=r"^\d{14}$", description="조회 타임스탬프 (예: 20240301120000)"
    )
    next_page: Optional[str] = Field(None, description="다음 페이지 기준값")
    limit: int = Field(..., ge=1, le=100, description="최대 조회 개수 (1~100)")
