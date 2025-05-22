from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from datetime import datetime
from app.core.deps import get_current_user

# 카드 목록 관련
from app.models.card_list import Card
from app.schemas.card_list import CardSchema

# 승인 내역 관리
from app.models.card_approval_domestic import CardApprovalDomestic
from app.schemas.card_approval_domestic import CardApprovalDomesticSchema

# 카드 청구 관련
from app.models.card_bill import CardBill
from app.schemas.card_bill import CardBillSchema

# 응답 스키마/유효성 검사
# 카드 목록
from app.schemas.card_response import CardListResponse
from app.schemas.card_list_request import CardListRequest
# 카드 청구
from app.schemas.card_bill_request import CardBillRequest
from app.schemas.card_bill_response import CardBillListResponse

# 카드 승인
from app.schemas.card_approval_domestic_response import CardApprovalDomesticResponse
from app.schemas.card_approval_domestic_request import CardApprovalDomesticRequest

from typing import List

router = APIRouter(
    prefix="/v1/card",
    tags=["Card"]
)

# 응답 스키마
# 카드 목록 관련 (응답 스키마 개별 적용)
@router.get("/cards", response_model=CardListResponse)
def get_cards(
    # 요청 파라미터 (필수 아니면 default=None)
    current_user: str = Depends(get_current_user),
    org_code: List[str] = Query(default=None, description="여러 org_code를 지정할 수 있습니다"),
    search_timestamp: str = Query(default=None),
    next_page: str = Query(default=None),
    limit: int = Query(...),
    req: CardListRequest = Depends(),
    db: Session = Depends(get_db),
    ):
    # 파라미터에 입력한 값을 비교하는 query
    query = db.query(Card).filter(Card.user_id == current_user)    
    if org_code:
        query = db.query(Card).filter(Card.user_id == current_user, Card.org_code.in_(org_code))
    if next_page:
        query = query.filter(Card.card_id > next_page)

    query = query.order_by(Card.card_id).limit(limit)
    cards = query.all()

    next_page_value = cards[-1].card_id if len(cards) == limit else None

    return {
        "rsp_code": "00000",
        "rsp_msg": "정상처리",
        "search_timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "card_cnt": len(cards),
        "card_list": cards,
        "next_page": next_page_value
    }

# 카드 승인 관련
@router.get("/cards/{card_id}/approval-domestic", response_model=CardApprovalDomesticResponse)
def get_domestic_approvals(
    card_id: str,
    current_user: str = Depends(get_current_user),
    from_date: str = Query(...),
    to_date: str = Query(...),
    next_page: str = Query(default=None),
    limit: int = Query(...),
    req: CardApprovalDomesticRequest = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(CardApprovalDomestic).filter(
        CardApprovalDomestic.user_id == current_user,
        CardApprovalDomestic.card_id == card_id,
        CardApprovalDomestic.approved_dtime >= from_date,
        CardApprovalDomestic.approved_dtime <= to_date
    )

    if next_page:
        query = query.filter(CardApprovalDomestic.approved_dtime > next_page)

    query = query.order_by(CardApprovalDomestic.approved_dtime).limit(limit)
    approvals = query.all()

    next_page_value = approvals[-1].approved_dtime if len(approvals) == limit else None

    return {
        "rsp_code": "00000",
        "rsp_msg": "정상처리",
        "approved_cnt": len(approvals),
        "approved_list": approvals,
        "next_page": next_page_value
    }


# 카드 지불 관련
@router.get("/bills", response_model=CardBillListResponse)
def get_card_bills(
    current_user: str = Depends(get_current_user),
    org_code: str = Query(...),
    from_month: str = Query(...),
    to_month: str = Query(...),
    next_page: str = Query(default=None),
    limit: int = Query(...),
    req: CardBillRequest = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(CardBill).filter(
        CardBill.user_id == current_user,
        CardBill.charge_month >= from_month,
        CardBill.charge_month <= to_month
    )

    if next_page:
        query = query.filter(CardBill.charge_month > next_page)

    query = query.order_by(CardBill.charge_month).limit(limit)
    bills = query.all()

    next_page_value = bills[-1].charge_month if len(bills) == limit else None

    return {
        "rsp_code": "00000",
        "rsp_msg": "정상처리",
        "bill_cnt": len(bills),
        "bill_list": bills,
        "next_page": next_page_value
    }
