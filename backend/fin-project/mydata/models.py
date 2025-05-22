# Create your models here.
from django.db import models

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
    
    card_id = models.CharField(max_length=100, primary_key=True, help_text="카드 식별자")
    masked_card_number = models.CharField(max_length=20, help_text="마스킹된 카드번호")
    card_name = models.CharField(max_length=100, help_text="카드상품명")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, help_text="카드구분")
    owner_type = models.CharField(max_length=10, choices=OWNER_TYPE_CHOICES, help_text="본인/가족 구분")
    org_code = models.CharField(max_length=20, help_text="기관명")
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.card_name} ({self.masked_card_number})"
    
    class Meta:
        verbose_name = "카드"
        verbose_name_plural = "카드 목록"
        
        
class CardApproval(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('01', '승인'),
        ('02', '승인취소'),
        ('03', '대기'),
        ('04', '무승인매입'),
        # 필요 시 추가
    )
    
    USAGE_TYPE_CHOICES = (
        ('01', '신용'),
        ('02', '체크'),
        # 필요 시 추가
    )
    
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='approvals', help_text="연결된 카드")
    approval_number = models.CharField(max_length=50, primary_key=True, help_text="승인번호")
    approval_datetime = models.DateTimeField(help_text="승인일시")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, help_text="결제상태")
    usage_type = models.CharField(max_length=20, choices=USAGE_TYPE_CHOICES, help_text="사용구분")
    merchant_name = models.CharField(max_length=100, help_text="가맹점명(소비처)")
    business_number = models.CharField(max_length=20, null=True, blank=True, help_text="사업자등록번호")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="이용금액")
    installment_count = models.PositiveSmallIntegerField(default=0, help_text="할부회차 (0은 일시불)")
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.merchant_name} ({self.amount}원) - {self.approval_datetime.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "카드 승인내역"
        verbose_name_plural = "카드 승인내역 목록"
        unique_together = ('card', 'approval_number')  # 카드와 승인번호의 조합은 유일해야 함
        indexes = [
            models.Index(fields=['card', 'approval_datetime']),  # 조회 성능 향상을 위한 인덱스
        ]
        

# 카드 청구
class CardBill(models.Model):
    bill_year_month = models.CharField(max_length=6, help_text="청구년월 (YYYYMM)")
    payment_year_month_day = models.CharField(max_length=8, help_text="결제년월일 (YYYYMMDD)")
    payment_date = models.DateField(help_text="결제일")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="월별 청구금액")
    
    # 청구서와 카드들의 관계 (다대다 관계)
    cards = models.ManyToManyField(Card, through='CardBillDetail', related_name='bills')
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bill_year_month} 청구서 ({self.total_amount}원)"
    
    class Meta:
        verbose_name = "카드 청구서"
        verbose_name_plural = "카드 청구서 목록"


class CardBillDetail(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, help_text="연결된 카드")
    bill = models.ForeignKey(CardBill, on_delete=models.CASCADE, related_name='details', help_text="연결된 청구서")
    amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="해당 카드의 청구금액")
    
    # 메타데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.card.card_name} - {self.bill.bill_year_month} ({self.amount}원)"
    
    class Meta:
        verbose_name = "카드별 청구 상세"
        verbose_name_plural = "카드별 청구 상세 목록"
        unique_together = ('card', 'bill')  # 카드와 청구서의 조합은 유일해야 함