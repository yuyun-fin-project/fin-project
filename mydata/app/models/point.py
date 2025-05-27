from sqlalchemy import Column, String, Float
from app.core.database import Base

class Point(Base):
    __tablename__ = "points"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    org_code = Column(String, nullable=False)
    search_timestamp = Column(String, nullable=False)

    point_name = Column(String)
    remain_point_amt = Column(Float)
    expiring_point_amt = Column(Float)
