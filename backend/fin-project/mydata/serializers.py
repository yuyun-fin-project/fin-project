from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    card_num = serializers.CharField()
    card_type = serializers.CharField()
    card_member = serializers.CharField()
    org_code = serializers.CharField()
    
    class Meta:
        model = Card
        fields = ['card_id', 'card_num', 'card_name', 'card_type', 'card_member', 'org_code'] # 메타데이터 제외