from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user

# 선불카드 잔액 관련
from app.models.prepaid_balance import PrepaidBalance
from app.schemas.prepaid_balance import PrepaidBalanceSchema
from app.schemas.prepaid_balance_response import PrepaidBalanceResponse

# 선불카드 승인 관련
from app.models.prepaid_approval import PrepaidApproval
from app.schemas.prepaid_approval import PrepaidApprovalSchema
from app.schemas.prepaid_approval_response import PrepaidApprovalResponse

# 요청 파라미터
from app.schemas.prepaid_balance_request import PrepaidBalanceRequest
from app.schemas.prepaid_approval_request import PrepaidApprovalRequest

from typing import List


router = APIRouter(
    prefix="/v1/card/prepaid",
    tags=["Prepaid Cards"]
)

# 선불카드 잔액

@router.post("/balance", response_model=PrepaidBalanceResponse)
def get_prepaid_balance(
    req: PrepaidBalanceRequest, 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    row = db.query(PrepaidBalance).filter(
        PrepaidBalance.user_id == "user123",  # 필요 시 token 또는 user_id 추출
        PrepaidBalance.pp_id == req.pp_id,
        PrepaidBalance.search_timestamp == req.search_timestamp
    ).first()

    if not row:
        raise HTTPException(status_code=404, detail="선불카드 잔액 정보가 없습니다.")

    return {
        "rsp_code": "00000",
        "rsp_msg": "정상처리",
        "search_timestamp": row.search_timestamp,
        "total_balance_amt": row.total_balance_amt,
        "charge_balance_amt": row.charge_balance_amt or 0,
        "reserve_balance_amt": row.reserve_balance_amt or 0,
        "reserve_due_amt": row.reserve_due_amt or 0,
        "exp_due_amt": row.exp_due_amt
    }

# 선불카드 승인
@router.post("/approval", response_model=PrepaidApprovalResponse)
def get_prepaid_approvals(
    req: PrepaidApprovalRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    query = db.query(PrepaidApproval).filter(
        PrepaidApproval.user_id == "user123",
        PrepaidApproval.approved_dtime >= req.from_date,
        PrepaidApproval.approved_dtime <= req.to_date
    )

    if req.next_page:
        query = query.filter(PrepaidApproval.approved_num > req.next_page)

    results = query.order_by(PrepaidApproval.approved_num).limit(req.limit).all()
    
    # 페이징 처리하기
    next_page_value = results[-1].approved_num if len(results) == req.limit else None

    return {
        "rsp_code": "00000",
        "rsp_msg": "정상처리",
        "approved_cnt": len(results),
        "approved_list": results,
        "next_page": next_page_value
    }
