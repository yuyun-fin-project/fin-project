from django.db import models

# Create your models here.
class Product(models.Model):
    prd_name = models.CharField(max_length=100)
    ord_num = models.CharField(max_length=100)
    mtrt_int = models.CharField(max_length=100, default=0)
    join_deny = models.CharField(max_length=10)
    prd_type = models.CharField(max_length=10)
    dcls_strt_dat = models.DateTimeField()
    scls_end_dat = models.DateTimeField()

    

class Option(models.Model):
    """저축 금리 정보 테이블"""
    prd = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='savings_rates')
    intr_rate_type = models.CharField(max_length=100)
    intr_rate_type_nm = models.CharField(max_length=100)
    rsrv_type = models.CharField(max_length=100, blank=True, null=True)
    rsrv_type_nm = models.CharField(max_length=100, blank=True, null=True)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    ord_num = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'savings_rate'
    
    def __str__(self):
        return f"{self.prd} - {self.intr_rate_type_nm}"