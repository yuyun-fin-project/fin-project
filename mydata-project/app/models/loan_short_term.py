from sqlalchemy import Column, String, Float
from app.core.database import Base

class LoanShortTerm(Base):
    __tablename__ = "loan_short_term"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    org_code = Column(String, nullable=False)
    search_timestamp = Column(String, nullable=False)

    loan_dtime = Column(String)
    loan_amt = Column(Float)
    balance_amt = Column(Float)
    pay_due_date = Column(String)
    int_rate = Column(Float)
