from pydantic import BaseModel

class LoanLongTermSchema(BaseModel):
    id: str
    user_id: str
    org_code: str
    search_timestamp: str
    loan_num: str
    loan_dtime: str
    loan_type: str
    loan_name: str
    loan_amt: float
    int_rate: float
    exp_date: str
    balance_amt: float
    repay_method: str
    int_amt: float

    class Config:
        from_attributes = True
