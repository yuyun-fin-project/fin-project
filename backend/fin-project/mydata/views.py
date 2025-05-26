from django.shortcuts import render
from django.http import JsonResponse

from .utils.api_clients.mydata_api import get_card_list, get_card_approval,get_bill
from .utils.data_processors.my_data_cleaner import data_preprocessing

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CardApprovalSerializer, CardSerializer, CardBillSerializer
from .models import Card, CardApproval, CardBill


import requests
from openai import OpenAI
from django.conf import settings
import os
import re
import json
from dotenv import load_dotenv


def extract_json(text):
    # ```json ... ``` 제거
    return re.sub(r"```json\n|\n```", "", text).strip()



# Create your views here.
@api_view(['POST', 'GET'])
def get_mydata(request):
    card_list = get_card_list(request)
    cleaned_card_list, jwt_token = data_preprocessing(card_list, 'cards')
    serializer = CardSerializer(data=cleaned_card_list, many=True)
    try:
        if serializer.is_valid(raise_exception=True):
            # 새로운 카드만 추가하고 기존 카드는 업데이트
            for card_data in serializer.validated_data:
                card_id = card_data.get('card_id')
                # 동일한 card_id가 있는지 확인
                card, created = Card.objects.update_or_create(
                    card_id=card_id,
                    defaults={
                        'user': request.user,
                        'card_num': card_data.get('card_num'),
                        'card_name': card_data.get('card_name'),
                        'card_type': card_data.get('card_type'),
                        'card_member': card_data.get('card_member'),
                        'org_code': card_data.get('org_code')
                    }
                )
                if created:
                    print(f"새 카드 추가: {card_id}")
                else:
                    print(f"기존 카드 업데이트: {card_id}")
    except Exception as e:
        print("유효성 실패:", serializer.errors)
        raise e
    
    # 사용자의 모든 카드 가져오기
    user_cards = Card.objects.filter(user=request.user)
    
    for card in user_cards:
        card_approval = get_card_approval(jwt_token, card.card_id)
        cleaned_approval_list = data_preprocessing(card_approval, 'approvals')
        
        # 카드 승인 내역 처리
        serializer = CardApprovalSerializer(data=cleaned_approval_list, many=True)
        if serializer.is_valid(raise_exception=True):
            for approval_data in serializer.validated_data:
                approved_num = approval_data.get('approved_num')
                # 동일한 승인번호가 있는지 확인
                if not CardApproval.objects.filter(
                    card_id=card,
                    approved_num=approved_num
                ).exists():
                    # 새로운 승인 내역 추가
                    CardApproval.objects.create(card_id=card, **approval_data)
                    print(f"새 승인 내역 추가: {approved_num}")
                else:
                    print(f"이미 존재하는 승인 내역: {approved_num}")
    
    bills_data = get_bill(jwt_token)
    serializer = CardBillSerializer(data=bills_data.get('bill_list', []), many=True)
    if serializer.is_valid(raise_exception=True):
        for bill_data in serializer.validated_data:
            bill_year_month = bill_data.get('bill_year_month')
            org_code = bill_data.get('org_code')
            # 동일한 사용자, 동일한 청구월, 동일한 기관의 데이터가 있는지 확인
            if not CardBill.objects.filter(
                user=request.user,
                bill_year_month=bill_year_month,
                org_code=org_code
            ).exists():
                # 새로운 데이터 추가
                CardBill.objects.create(user=request.user, **bill_data)
            else:
                print(f"이미 존재하는 청구서 데이터: {bill_year_month}, {org_code}")
    
    # Get cards for the current user
    cards = Card.objects.filter(user=request.user)
    print(f"Found {cards.count()} cards for user {request.user.id}")
    serializer = CardSerializer(cards, many=True)
    
    # Get card approvals for the user's cards
    card_approvals = CardApproval.objects.filter(card_id__in=cards)
    print(f"Found {card_approvals.count()} card approvals")
    
    # Get card bills for the user's cards
    card_bills = CardBill.objects.filter(user=request.user)
    print(f"Found {card_bills.count()} card bills")

    return Response({
        'card_list': serializer.data,
        'card_approvals': [{
            'id': approval.id,
            'card_id': approval.card_id_id,
            'approved_num': approval.approved_num,
            'approved_dtime': approval.approved_dtime,
            'approved_amt': approval.approved_amt,
            'merchant_name': approval.merchant_name,
            'status': approval.get_status_display(),
            'total_install_cnt': approval.total_install_cnt
        } for approval in card_approvals],
        'card_bills': [{
            'id': bill.id,
            'org_code': bill.org_code,
            'bill_year_month': bill.bill_year_month,
            'payment_year_month_day': bill.payment_year_month_day,
            'total_amount': bill.total_amount,
            'payment_date': bill.payment_date
        } for bill in card_bills],
    }, status=status.HTTP_200_OK)




def AI_input_data(request):
    cards = Card.objects.filter(user=request.user)
    serializer = CardSerializer(cards, many=True)
    
    # Get card approvals for the user's cards
    card_approvals = CardApproval.objects.filter(card_id__in=cards)
    
    # Get card bills for the user's cards
    card_bills = CardBill.objects.filter(user=request.user)
    if cards.count() == 0:
        return None
    return {
        'card_list': serializer.data,
        'card_approvals': [{
            'id': approval.id,
            'card_id': approval.card_id_id,
            'approved_num': approval.approved_num,
            'approved_dtime': approval.approved_dtime,
            'approved_amt': approval.approved_amt,
            'merchant_name': approval.merchant_name,
            'status': approval.get_status_display(),
            'total_install_cnt': approval.total_install_cnt
        } for approval in card_approvals],
        'card_bills': [{
            'id': bill.id,
            'org_code': bill.org_code,
            'bill_year_month': bill.bill_year_month,
            'payment_year_month_day': bill.payment_year_month_day,
            'total_amount': bill.total_amount,
            'payment_date': bill.payment_date
        } for bill in card_bills],
    }


load_dotenv()

# OpenAI 클라이언트 초기화 함수
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        # 임시 테스트용 더미 클라이언트 반환
        return None
    return OpenAI(api_key=api_key)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_and_recommend(request):
    if request.method == "POST":
        try:
            # 사용자 입력 (income) 받기
            data = AI_input_data(request)
            if data is None:
                return Response({"error": "No data found for the user"}, status=status.HTTP_404_NOT_FOUND)
            input_data = json.loads(request.body)
            income = input_data.get('income')
            # income = 2400000

            # 예시: 소비 데이터는 고정값 (DB에서 불러와야!)
            card_approvals = data.get('card_approvals', [])
            card_bills = data.get("card_bills")
            total_spent = sum(item["approved_amt"] for item in card_approvals)

            # 소비 요약
                        # 월간 소비 요약
            monthly_spending = {}
            for bill in card_bills:
                month = bill["bill_year_month"]
                monthly_spending[month] = monthly_spending.get(month, 0) + bill["total_amount"]

            # 세부 소비 내역 (간단 정리)
            detail_lines = []
            for approval in card_approvals:
                if approval["status"] == "승인":  # 승인된 것만
                    date = approval["approved_dtime"][:6]
                    detail_lines.append(
                        f"{date}: {approval['merchant_name']} ({approval['approved_amt']}원)"
                    )

            # GPT에게 보낼 프롬프트
            prompt = (
                f"사용자의 월 소득은 {income}원입니다.\n\n"
                f"월별 소비 요약:\n"
            )
            for month, amount in monthly_spending.items():
                prompt += f"- {month}: {amount}원\n"

            prompt += "\n소비 상세 내역:\n" + "\n".join(detail_lines)  # 일부만

            prompt +="""너는 사용자의 소비 데이터를 기반으로 금융 조언을 해주는 한국어 금융설계 전문가입니다.
                
                사용자의 월 소득: {income}원
                월별 소비: {monthly_spending}
                세부 소비 내역: {detail_lines}

                아래 데이터를 기반으로 반드시 아래 항목들을 포함한 순수 JSON 형태로 한국어로 답변해주세요.
                절대로 코드블록(예: ```json, ```)이나 다른 문자 태그를 붙이지 말고, 아래처럼 순수 JSON으로만 작성해 주세요.

                반드시 포함해야 하는 항목:
                - current_spending: "현재 소비 금액 (예: 1,200,000원)"
                - unnecessary_items: ["불필요한 소비 항목1", "불필요한 소비 항목2", ...]
                - possible_reduction: "감축할 수 있는 금액 (예: 200,000원)"
                - income_spending_ratio: "소득 대비 소비율 (예: 소득의 45%를 소비하고 있습니다.)"
                - emergency_saving_advice: "비상금 저축 권장 내용 (예: 월 소득의 10%인 240,000원을 비상금으로 저축해보세요.)"
                - card_spending_focus: "특정 카드의 지출 집중도 (예: 현대카드에서 월 400,000원 이상 지출 중입니다.)"
                - spending_trend: "최근 월별 지출 추이 비교 (예: 4월 소비가 3월보다 20% 증가했습니다.)"
                - subscription_check: "불필요한 정기 결제 서비스 조언 (예: 넷플릭스, 멜론 구독을 재검토해보세요.)"
                - recommendation: "종합적인 절약 및 저축 방안 제안"
                
                예시:
                {
                "current_spending": "1,200,000원",
                "unnecessary_items": ["고급 커피", "불필요한 외식",...],
                "possible_reduction": "200,000원",
                "income_spending_ratio": "소득의 45%를 소비하고 있습니다.",
                "emergency_saving_advice": "월 소득의 10%인 240,000원을 비상금으로 저축해보세요.",
                "card_spending_focus": "주로 현대카드에서 월 400,000원 이상 지출 중입니다.",
                "spending_trend": "4월 소비가 3월보다 20% 증가했습니다.",
                "subscription_check": "넷플릭스, 멜론 등 불필요한 정기 결제 서비스를 재검토해보세요.",
                "recommendation": "외식을 주 1회로 줄이고, 고급 커피 대신 집에서 간편한 커피를 마셔보세요. 자동이체를 활용해 저축을 시작해보세요."
                }
                예시를 그대로 쓰지 말고 소비 내역을 보고 적절하게 작성해줘


                반드시 순수 JSON 형식으로만 답변해 주세요.
                """


            # OpenAI 클라이언트 가져오기
            client = get_openai_client()
            if not client:
                return JsonResponse({"error": "OpenAI API 키가 설정되지 않았습니다."}, status=500)
                
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "너는 사용자의 소비 데이터를 기반으로 금융 조언을 해주는 한국어 상담사입니다."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            recommendation_json = json.loads(response.choices[0].message.content)
            return Response({
                "monthly_spending": monthly_spending,
                "recommendation": recommendation_json
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)