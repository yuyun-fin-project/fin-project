from pydantic import BaseModel

class PointSchema(BaseModel):
    id: str
    user_id: str
    org_code: str
    search_timestamp: str
    point_name: str
    remain_point_amt: float
    expiring_point_amt: float

    class Config:
        from_attributes = True
