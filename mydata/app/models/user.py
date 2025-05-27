from sqlalchemy import Column, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=False, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)
