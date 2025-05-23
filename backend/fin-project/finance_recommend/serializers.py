from rest_framework import serializers
from .models import Product, Option

class ProductSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Article
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__' 