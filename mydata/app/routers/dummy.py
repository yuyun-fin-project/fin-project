# 더마데이터 생성하기

# app/routers/dummy.py
from fastapi import APIRouter, HTTPException, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Dummy
from app.core.security import hash_password, verify_password, create_access_token
from app.services.generate_user_data import generate_user_dummy_data
from app.models.card_list import Card
import uuid

router = APIRouter(prefix="/generate", tags=["Dummy"])

@router.post("/")
def generate(user: Dummy, db: Session = Depends(get_db)):
    card_list={} 
    # 아이디 존재 여부 조회
    user_obj = db.query(User).filter(User.email == user.useremail).first()
    if user_obj:
        query = db.query(Card).filter(Card.user_id == user_obj.id)
        message = "data load success"
        # raise HTTPException(status_code=400, detail="User already exists")
    else:
        # 새계정 생성 및 db에 추가
        new_user = User(
            id=str(uuid.uuid4()),
            username=user.username,
            email= user.useremail,
            hashed_password=hash_password('test1234')
        )
        db.add(new_user)
        db.commit()
        
        # db에서 생성한 user 객체 선언
        user_obj = db.query(User).filter(User.email == user.useremail).first()
        
        # DB 세션 전달
        generate_user_dummy_data(user_obj)
        query = db.query(Card).filter(Card.user_id == user_obj.id)
        message = "data_generate_success"
    
    # & 토큰 생성
    token = create_access_token(data={"user_id": user_obj.id})
    card_list = query.all()
    return {
        "msg": message, 
        "access_token": token,
        "data": card_list,
        }