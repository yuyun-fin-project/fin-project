from sqlalchemy import Column, String, Float
from app.core.database import Base

class LoanLongTerm(Base):
    __tablename__ = "loan_long_term"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    org_code = Column(String, nullable=False)
    search_timestamp = Column(String, nullable=False)

    loan_num = Column(String)
    loan_dtime = Column(String)
    loan_type = Column(String)
    loan_name = Column(String)
    loan_amt = Column(Float)
    int_rate = Column(Float)
    exp_date = Column(String)
    balance_amt = Column(Float)
    repay_method = Column(String)
    int_amt = Column(Float)
