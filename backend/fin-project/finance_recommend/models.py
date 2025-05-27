from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
# Create your models here.
class Product(models.Model):
    join_deny = models.CharField(
        max_length=10,
        choices=(
            (1, "제한없음"), 
            (2, "서민전용"), 
            (3, "일부제한")
        ),
    )

    """저축 상품 정보 테이블"""
    fin_prdt_nm = models.CharField(max_length=100)
    ord_num = models.CharField(max_length=100)
    fin_prdt_cd = models.CharField(max_length=100)
    kor_co_nm = models.CharField(max_length=100)
    mtrt_int = models.TextField()
    spcl_cnd = models.TextField(null=True, blank=True)
    etc_note = models.TextField(null=True, blank=True)
    join_member = models.CharField(max_length=100, null=True, blank=True)
    join_way = models.CharField(max_length=100, null=True, blank=True)
    prd_type = models.CharField(max_length=10) # "D": 정기예금, "S": 저축상품
    dcls_strt_dat = models.DateField(null=True)
    dcls_end_dat = models.DateField(null=True)
    fin_co_subm_day = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Option(models.Model):
    """저축 금리 정보 테이블"""
    prd = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    intr_rate_type = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100)
    rsrv_type = models.CharField(max_length=100, blank=True, null=True)
    rsrv_type_nm = models.CharField(max_length=100, blank=True, null=True)
    save_trm = models.CharField(max_length=100, blank=True, null=True)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.prd} - {self.intr_rate_type_nm}"


class Gold(models.Model):
    SPOT_TYPES = [
        ('GOLD', '금'),
    ]
    spot_type = models.CharField('상품구분', max_length=10, choices=SPOT_TYPES)
    itms_nm = models.CharField('품목명', max_length=100, null=True, blank=True)
    bas_dt = models.DateField('기준일자', db_index=True)  # API 응답의 basDt와 매핑
    clpr = models.DecimalField('종가', max_digits=15, decimal_places=2, null=True, blank=True)
    flt_rt = models.DecimalField('등락율', max_digits=15, decimal_places=2, null=True, blank=True)
    hipr = models.DecimalField('고가', max_digits=15, decimal_places=2, null=True, blank=True)
    lopr = models.DecimalField('저가', max_digits=15, decimal_places=2, null=True, blank=True)
    mkp = models.DecimalField('시가', max_digits=15, decimal_places=2, null=True, blank=True)
    tr_prc = models.DecimalField('거래대금', max_digits=20, decimal_places=2, null=True, blank=True)
    trqu = models.DecimalField('거래량', max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_spot_type_display()} - {self.bas_dt}"


class Oil(models.Model):
    SPOT_TYPES = [
        ('OIL', '유가'),
    ]
    spot_type = models.CharField('상품구분', max_length=10, choices=SPOT_TYPES)
    bas_dt = models.DateField('기준일자', db_index=True)  # API 응답의 basDt와 매핑
    oil_ctg = models.CharField('유종', max_length=20, null=True, blank=True)  # 경유, 휘발유 등
    wt_avg_prc_cptn = models.DecimalField('가중평균가격(전체)', max_digits=15, decimal_places=2, null=True, blank=True)
    wt_avg_prc_disc = models.DecimalField('가중평균가격(할인)', max_digits=15, decimal_places=2, null=True, blank=True)
    trqu = models.DecimalField('거래량', max_digits=20, decimal_places=2, null=True, blank=True)
    tr_prc = models.DecimalField('거래대금', max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.get_spot_type_display()} - {self.bas_dt}"


class Carbon(models.Model):
    SPOT_TYPES = [
        ('CARBON', '탄소배출권'),
    ]
    spot_type = models.CharField('상품구분', max_length=10, choices=SPOT_TYPES)
    bas_dt = models.DateField('기준일자', db_index=True)  # API 응답의 basDt와 매핑
    itms_nm = models.CharField('품목명', max_length=100, null=True, blank=True)
    clpr = models.DecimalField('종가', max_digits=15, decimal_places=2, null=True, blank=True)
    flt_rt = models.DecimalField('등락율', max_digits=15, decimal_places=2, null=True, blank=True)
    hipr = models.DecimalField('고가', max_digits=15, decimal_places=2, null=True, blank=True)
    lopr = models.DecimalField('저가', max_digits=15, decimal_places=2, null=True, blank=True)
    mkp = models.DecimalField('시가', max_digits=15, decimal_places=2, null=True, blank=True)
    tr_prc = models.DecimalField('거래대금', max_digits=20, decimal_places=2, null=True, blank=True)
    trqu = models.DecimalField('거래량', max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_spot_type_display()} - {self.bas_dt}" 


class ProductBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class SpotProduct(models.Model):
    spot_type = models.CharField(max_length=20, choices=[
        ('Gold', '금'),
        ('Oil', '유가'),
        ('Carbon', '탄소배출권')
    ])
    name = models.CharField(max_length=100)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    spot_object = GenericForeignKey('content_type', 'object_id')


class SpotProductBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spot_product = models.ForeignKey(SpotProduct, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'spot_product')