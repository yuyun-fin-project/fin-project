# app/schemas/point_request.py

from pydantic import BaseModel, Field

class PointRequest(BaseModel):
    org_code: str = Field(..., min_length=2, max_length=10, pattern=r"^[A-Z]+$", description="기관 코드 (대문자)")
    search_timestamp: str = Field(..., pattern=r"^\d{14}$", description="조회 타임스탬프 (YYYYMMDDHHMMSS)")
