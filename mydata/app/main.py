# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
# from app.models import card_approval
# from app.routers import card_approval
from app.routers import card, prepaid, asset, auth, dummy
from app.models.user import User


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# include_router 메서드 : app instance에 API라우터 추가
# app.include_router(card_approval.router)
app.include_router(card.router)
app.include_router(prepaid.router)
app.include_router(asset.router)
app.include_router(auth.router)
app.include_router(dummy.router)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello from Custom MyData API"}
