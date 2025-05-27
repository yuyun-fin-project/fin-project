from enum import unique
from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.db.models import CASCADE


# Create your models here.

class Card(models.Model):
    CARD_TYPE_CHOICES = (
        ('01', '신용'),
        ('02', '체크(직불포함)'),
        ('03', '소액신용체크'),
        # 필요 시 추가
    )
    
    OWNER_TYPE_CHOICES = (
        ('1', '본인'),
        ('2', '가족'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='cards')
    card_id = models.CharField(max_length=100, help_text="카드 식별자")
    card_num = models.CharField(max_length=20, help_text="카드번호")
    card_name = models.CharField(max_length=100, help_text="카드상품명")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, help_text="카드구분")
    card_member = models.CharField(max_length=10, choices=OWNER_TYPE_CHOICES, help_text="본인/가족 구분")
    org_code = models.CharField(max_length=20, help_text="기관명")
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.card_name} ({self.card_num})"
    
    class Meta:
        verbose_name = "카드"
        verbose_name_plural = "카드 목록"
        

class CardApproval(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('01', '승인'),
        ('02', '승인취소'),
        ('03', '대기'),
        ('04', '무승인매입'),
    )

    USAGE_TYPE_CHOICES = (
        ('01', '신용'),
        ('02', '체크'),
    )

    # FK를 User 모델로 연결 (또는 카드 모델이 있다면 그걸로!)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card_approvals')
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_approvals')
    approved_num = models.CharField(max_length=50, help_text="승인번호")
    approved_dtime = models.CharField(max_length=14, help_text="승인일시 (yyyyMMddHHmm 형식)")
    status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, help_text="결제 상태")
    pay_type = models.CharField(max_length=2, choices=USAGE_TYPE_CHOICES, help_text="사용 구분")
    
    merchant_name = models.CharField(max_length=100, help_text="가맹점명")
    merchant_regno = models.CharField(max_length=20, null=True, blank=True, help_text="사업자등록번호")
    approved_amt = models.DecimalField(max_digits=15, decimal_places=2, help_text="이용금액")
    total_install_cnt = models.PositiveSmallIntegerField(null=True, blank=True, help_text="할부회차 (null은 일시불)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.merchant_name} ({self.approved_amt}원) - {self.approved_dtime}"

    class Meta:
        verbose_name = "카드 승인내역"
        verbose_name_plural = "카드 승인내역 목록"
        indexes = [
            models.Index(fields=['card_id','approved_num']),
        ]


# 카드 청구
class CardBill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card_bills')
    org_code = models.CharField(max_length=20, help_text="기관코드")
    bill_year_month = models.CharField(max_length=6, null=True, blank=True, help_text="청구년월 (YYYYMM)")
    payment_year_month_day = models.CharField(max_length=8, null=True, blank=True, help_text="결제년월일 (YYYYMMDD)")
    payment_date = models.DateField(help_text="결제일", null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="월별 청구금액")
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bill_year_month} 청구서 ({self.total_amount}원)"
    
    class Meta:
        verbose_name = "카드 청구서"
        verbose_name_plural = "카드 청구서 목록"