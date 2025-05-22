from pydantic import BaseModel
from typing import Optional

class PrepaidApprovalRequest(BaseModel):
    org_code: str
    pp_id: str
    from_date: str
    to_date: str
    limit: int
    next_page: Optional[str] = None
