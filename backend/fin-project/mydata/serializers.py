from rest_framework import serializers
from .models import Card, CardApproval, CardBill

class CardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # PK 값 추가
    card_num = serializers.CharField()
    card_type = serializers.CharField()
    card_member = serializers.CharField()
    org_code = serializers.CharField()
    
    class Meta:
        model = Card
        fields = ['id', 'card_id', 'card_num', 'card_name', 'card_type', 'card_member', 'org_code']

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        if not user:
            raise serializers.ValidationError({"user": "User is required"})

        instance, created = Card.objects.get_or_create(
            card_id=validated_data['card_id'],
            defaults={
                'user': user,
                'card_num': validated_data.get('card_num'),
                'card_name': validated_data.get('card_name'),
                'card_type': validated_data.get('card_type'),
                'card_member': validated_data.get('card_member'),
                'org_code': validated_data.get('org_code')
            }
        )
        
        # 이미 존재하는 카드인 경우 업데이트
        if not created:
            update_fields = ['card_num', 'card_name', 'card_type', 'card_member', 'org_code']
            for field in update_fields:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
            instance.user = user  # 사용자 정보도 업데이트
            instance.save()
        
        return instance

class CardApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardApproval
        fields = '__all__'
        read_only_fields = ('card_id',)
    
    def create(self, validated_data):
        # Get unique identifying fields for CardApproval
        # Adjust these fields based on what makes a CardApproval unique
        unique_fields = {
            'approval_num': validated_data.get('approval_num'),
            # Add other fields that uniquely identify a CardApproval
        }
        
        # Filter out None values from unique_fields
        unique_fields = {k: v for k, v in unique_fields.items() if v is not None}
        
        if unique_fields:
            instance, created = CardApproval.objects.update_or_create(
                **unique_fields,
                defaults=validated_data
            )
            return instance
        return super().create(validated_data)



class CardBillSerializer(serializers.ModelSerializer):
    charge_amt = serializers.DecimalField(source='total_amount', max_digits=15, decimal_places=2)
    charge_day = serializers.CharField(source='payment_year_month_day')
    charge_month = serializers.CharField(source='bill_year_month')
    paid_out_date = serializers.CharField(source='payment_date')
    org_code = serializers.CharField()

    class Meta:
        model = CardBill
        fields = ['id', 'user_id', 'charge_amt', 'charge_day', 'charge_month', 'paid_out_date', 'org_code']

    def get_paid_out_date(self, obj):
        return obj.payment_date.strftime("%Y%m%d") if obj.payment_date else None

    def create(self, validated_data):
        # 사용자 정보 가져오기 (요청 컨텍스트에서)
        user = self.context.get('request').user if self.context.get('request') else None
        if not user or user.is_anonymous:
            raise serializers.ValidationError({"user": "User is required"})
            
        # 필드 매핑 처리
        total_amount = validated_data.pop('total_amount', None)
        payment_year_month_day = validated_data.pop('payment_year_month_day', None)
        bill_year_month = validated_data.pop('bill_year_month', None)
        payment_date = validated_data.pop('payment_date', None)
        
        # 청구서 생성
        instance = CardBill.objects.create(
            user=user,
            total_amount=total_amount,
            payment_year_month_day=payment_year_month_day,
            bill_year_month=bill_year_month,
            payment_date=payment_date,
            **validated_data
        )
        return instance