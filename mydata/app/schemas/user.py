from pydantic import BaseModel, EmailStr

class Dummy(BaseModel):
    username: str
    useremail: EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    useremail: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str
    useremail: EmailStr
