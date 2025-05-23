from rest_framework import serializers
from .models import CustomUser
from articles.serializers import ArticleSerializer, CommentSerializer

# articles/models 안의 모델


class UserSerializes(serializers.ModelSerializer):
    
    articles = ArticleSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'username', 'useremai', 'articles', 'comments']