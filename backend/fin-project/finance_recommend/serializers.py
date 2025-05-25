from rest_framework import serializers
from .models import Product, Option, Gold, Oil, Carbon
from .utils.cosine_similarity import recommend_products

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        instance, created = Product.objects.get_or_create(
            fin_prdt_cd=validated_data['fin_prdt_cd'],
            defaults={'fin_prdt_nm': validated_data.get('fin_prdt_nm'),
            'ord_num': validated_data.get('ord_num'),
            'prd_type': validated_data.get('prd_type'),
            'dcls_strt_dat': validated_data.get('dcls_strt_dat'),
            'dcls_end_dat': validated_data.get('dcls_end_dat'),
            'fin_co_subm_day': validated_data.get('fin_co_subm_day'),
            'join_deny': validated_data.get('join_deny'),
            'join_member': validated_data.get('join_member'),
            'join_way': validated_data.get('join_way'),
            'mtrt_int': validated_data.get('mtrt_int'),
            'spcl_cnd': validated_data.get('spcl_cnd'),
            'etc_note': validated_data.get('etc_note'),
            'created_at': validated_data.get('created_at'),
            'updated_at': validated_data.get('updated_at'),
            'kor_co_nm': validated_data.get('kor_co_nm'),
            }
        )
        if not created:
            instance.fin_prdt_nm = validated_data.get('fin_prdt_nm', instance.fin_prdt_nm)
            instance.ord_num = validated_data.get('ord_num', instance.ord_num)
            instance.prd_type = validated_data.get('prd_type', instance.prd_type)
            instance.dcls_strt_dat = validated_data.get('dcls_strt_dat', instance.dcls_strt_dat)
            instance.dcls_end_dat = validated_data.get('dcls_end_dat', instance.dcls_end_dat)
            instance.fin_co_subm_day = validated_data.get('fin_co_subm_day', instance.fin_co_subm_day)
            instance.join_deny = validated_data.get('join_deny', instance.join_deny)
            instance.join_member = validated_data.get('join_member', instance.join_member)
            instance.join_way = validated_data.get('join_way', instance.join_way)
            instance.mtrt_int = validated_data.get('mtrt_int', instance.mtrt_int)
            instance.spcl_cnd = validated_data.get('spcl_cnd', instance.spcl_cnd)
            instance.etc_note = validated_data.get('etc_note', instance.etc_note)
            instance.kor_co_nm = validated_data.get('kor_co_nm', instance.kor_co_nm)
            instance.save()
        return instance


class OptionSerializer(serializers.ModelSerializer):
    
    prd = serializers.PrimaryKeyRelatedField(read_only=True)
    fin_prdt_cd = serializers.CharField(write_only=True)

    class Meta:
        model = Option
        fields = [
            'id',
            'fin_prdt_cd',  # 클라이언트에서만 쓰고 DB에는 저장하지 않음
            'prd',
            'intr_rate_type',
            'intr_rate_type_nm',
            'rsrv_type',
            'rsrv_type_nm',
            'intr_rate',
            'intr_rate2',
        ]

    def create(self, validated_data):
        # fin_prdt_cd 꺼내서 prd 찾기
        fin_prdt_cd = validated_data.pop('fin_prdt_cd')

        try:
            product = Product.objects.get(fin_prdt_cd=fin_prdt_cd)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'fin_prdt_cd': '해당 fin_prdt_cd를 가진 Product가 존재하지 않습니다.'})

        # prd로 연결해서 Option 저장
        option = Option.objects.create(prd=product, **validated_data)
        return option

'''
{'basDt': '20250522',
'clpr': '148100',
'fltRt': '.09',200002',
'itmsNm': '금 99.99_1Kg',
'lopr': '147010',
'mkp': '147390',
'srtnCd': '04020000',
'trPrc': '21058218970',
'trqu': '142248',
'vs': '140'}
'hipr': '148700',
'isinCd': 'KRD040
'''
class GoldSerializer(serializers.ModelSerializer):
    spotType = serializers.CharField(source='spot_type', read_only=True)
    spotTypeNm = serializers.CharField(source='get_spot_type_display', read_only=True)
    itmsNm = serializers.CharField(source='itms_nm')
    basDt = serializers.DateField(source='bas_dt', format='%Y%m%d')
    clpr = serializers.DecimalField(max_digits=15, decimal_places=2)
    fltRt = serializers.DecimalField(source='flt_rt', max_digits=15, decimal_places=2)
    hipr = serializers.DecimalField(max_digits=15, decimal_places=2)
    lopr = serializers.DecimalField(max_digits=15, decimal_places=2)
    mkp = serializers.DecimalField( max_digits=15, decimal_places=2)
    trPrc = serializers.DecimalField(source='tr_prc', max_digits=15, decimal_places=2)
    trqu = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        model = Gold
        fields = [
            'id', 
            'spotType', 
            'spotTypeNm',
            'itmsNm',
            'basDt',
            'clpr',
            'fltRt',
            'hipr',
            'lopr',
            'mkp',
            'trPrc',
            'trqu',
            'created_at'
        ]
        read_only_fields = fields
    
    def create(self, validated_data):
        instance, created = Gold.objects.get_or_create(
            bas_dt=validated_data['bas_dt'],
            itms_nm=validated_data['itms_nm'],
            defaults={
                'spot_type': validated_data.get('spot_type'),
                'clpr': validated_data.get('clpr'),
                'flt_rt': validated_data.get('flt_rt'),
                'hipr': validated_data.get('hipr'),
                'lopr': validated_data.get('lopr'),
                'mkp': validated_data.get('mkp'),
                'tr_prc': validated_data.get('tr_prc'),
                'trqu': validated_data.get('trqu'),
            }
        )
        if not created:
            for field in ['clpr', 'flt_rt', 'hipr', 'lopr', 'mkp', 'tr_prc', 'trqu']:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
            instance.save()
        return instance


class OilSerializer(serializers.ModelSerializer):
    spotType = serializers.CharField(source='spot_type', read_only=True)
    spotTypeNm = serializers.CharField(source='get_spot_type_display', read_only=True)
    basDt = serializers.DateField(source='bas_dt', format='%Y%m%d')
    oilCtg = serializers.CharField(source='oil_ctg')
    wtAvgPrcCptn = serializers.DecimalField(source='wt_avg_prc_cptn', max_digits=15, decimal_places=2)
    wtAvgPrcDisc = serializers.DecimalField(source='wt_avg_prc_disc', max_digits=15, decimal_places=2)
    trqu = serializers.DecimalField(max_digits=20, decimal_places=2)
    trPrc = serializers.DecimalField(source='tr_prc', max_digits=20, decimal_places=2)

    class Meta:
        model = Oil
        fields = [
            'id', 
            'spotType', 
            'spotTypeNm',
            'basDt',
            'oilCtg',
            'wtAvgPrcCptn',
            'wtAvgPrcDisc',
            'trqu',
            'trPrc',
            'created_at'
        ]
        read_only_fields = fields
    
    def create(self, validated_data):
        instance, created = Oil.objects.get_or_create(
            bas_dt=validated_data['bas_dt'],
            oil_ctg=validated_data['oil_ctg'],
            defaults={
                'spot_type': validated_data.get('spot_type'),
                'wt_avg_prc_cptn': validated_data.get('wt_avg_prc_cptn'),
                'wt_avg_prc_disc': validated_data.get('wt_avg_prc_disc'),
                'trqu': validated_data.get('trqu'),
                'tr_prc': validated_data.get('tr_prc'),
                'trqu': validated_data.get('trqu'),
            }
        )
        if not created:
            for field in ['wt_avg_prc_cptn', 'wt_avg_prc_disc', 'trqu', 'tr_prc']:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
            instance.save()
        return instance

class CarbonSerializer(serializers.ModelSerializer):
    spotType = serializers.CharField(source='spot_type', read_only=True)
    spotTypeNm = serializers.CharField(source='get_spot_type_display', read_only=True)
    basDt = serializers.DateField(source='bas_dt', format='%Y%m%d')
    itmsNm = serializers.CharField(source='itms_nm')
    clpr = serializers.DecimalField(max_digits=15, decimal_places=2)
    fltRt = serializers.DecimalField(source='flt_rt', max_digits=15, decimal_places=2)
    hipr = serializers.DecimalField(max_digits=15, decimal_places=2)
    lopr = serializers.DecimalField(max_digits=15, decimal_places=2)
    mkp = serializers.DecimalField(max_digits=15, decimal_places=2)
    trPrc = serializers.DecimalField(source='tr_prc', max_digits=20, decimal_places=2)
    trqu = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = Carbon
        fields = [
            'id', 
            'spotType', 
            'spotTypeNm',
            'basDt',
            'itmsNm',
            'clpr',
            'fltRt',
            'hipr',
            'lopr',
            'mkp',
            'trPrc',
            'trqu',
            'created_at'
        ]
        read_only_fields = fields
    
    def create(self, validated_data):
        instance, created = Carbon.objects.get_or_create(
            bas_dt=validated_data['bas_dt'],
            itms_nm=validated_data['itms_nm'],
            defaults={
                'spot_type': validated_data.get('spot_type'),
                'clpr': validated_data.get('clpr'),
                'flt_rt': validated_data.get('flt_rt'),
                'hipr': validated_data.get('hipr'),
                'lopr': validated_data.get('lopr'),
                'mkp': validated_data.get('mkp'),
                'tr_prc': validated_data.get('tr_prc'),
                'trqu': validated_data.get('trqu'),
            }
        )
        if not created:
            for field in ['clpr', 'flt_rt', 'hipr', 'lopr', 'mkp', 'tr_prc', 'trqu']:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
            instance.save()
        return instance


class RecommendInputSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(choices=["D", "S"], default="D")
    save_trm = serializers.IntegerField(min_value=1, max_value=36, default=12)
    monthly_saving = serializers.IntegerField(min_value=1, max_value=1000, default=50)
    risk_level = serializers.ChoiceField(choices=["low", "medium", "high"], default="low")