from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    masked_card_number = serializers.CharField(source='card_num')
    card_type = serializers.CharField(source='card_type')
    owner_type = serializers.CharField(source='owner_type')
    org_code = serializers.CharField(source='org_code')
    
    class Meta:
        model = Card
        fields = ['card_id', 'masked_card_number', 'card_name', 'card_type', 'owner_type', 'org_code'] # 메타데이터 제외