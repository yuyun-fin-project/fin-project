from pydantic import BaseModel

class CardBillSchema(BaseModel):
    id: str
    user_id: str
    charge_amt: float
    charge_day: str
    charge_month: str
    paid_out_date: str

class Config:
    from_attributes = True