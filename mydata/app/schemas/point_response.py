from pydantic import BaseModel
from typing import List
from app.schemas.point import PointSchema

class PointListResponse(BaseModel):
    rsp_code: str = "00000"
    rsp_msg: str = "정상처리"
    search_timestamp: str
    point_cnt: int
    point_list: List[PointSchema]
