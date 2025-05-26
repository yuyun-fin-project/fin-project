from rest_framework import serializers
from .models import Article, Comment
# from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    # user_id = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'user_id', 'title', 'content', 'created_at', 'updated_at', 'nickname']

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__' 