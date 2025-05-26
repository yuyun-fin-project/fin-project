from django.shortcuts import render

# 테스트용 입니다.
from django.contrib.auth import get_user_model

from .utils.api_clients.mydata_api import get_card_list, get_card_approval,get_bill
from .utils.data_processors.my_data_cleaner import data_preprocessing

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .serializers import CardApprovalSerializer, CardSerializer, CardBillSerializer
from .models import Card, CardApproval, CardBill


import requests
from openai import OpenAI
from django.conf import settings
import os


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