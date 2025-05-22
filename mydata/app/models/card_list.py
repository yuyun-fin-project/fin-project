from sqlalchemy import Column, String, Boolean
from app.core.database import Base

class Card(Base):
    __tablename__ = "cards"

    card_id = Column(String, primary_key=True, index=True)
    card_num = Column(String, nullable=False)
    is_consent = Column(Boolean, default=True)
    card_name = Column(String)
    card_member = Column(String)
    card_type = Column(String)
    org_code = Column(String, nullable=False)
    user_id = Column(String, index=True, nullable=False)  # 사용자 식별자
