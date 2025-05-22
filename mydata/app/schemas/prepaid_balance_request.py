from pydantic import BaseModel

class PrepaidBalanceRequest(BaseModel):
    org_code: str
    pp_id: str
    search_timestamp: str
