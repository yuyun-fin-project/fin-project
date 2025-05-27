from pydantic import BaseModel

class CardSchema(BaseModel):
    card_id: str
    user_id: str
    card_num: str
    is_consent: bool
    card_name: str
    card_member: str
    card_type: str
    org_code: str

class Config:
    from_attributes = True
