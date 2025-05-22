from pydantic import BaseModel

class LoanShortTermSchema(BaseModel):
    id: str
    user_id: str
    org_code: str
    search_timestamp: str
    loan_dtime: str
    loan_amt: float
    balance_amt: float
    pay_due_date: str
    int_rate: float

    class Config:
        from_attributes = True
