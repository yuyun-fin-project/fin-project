from rest_framework import serializers
from .models import Article, Comment
# from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'user_id', 'title', 'content', 'created_at',
            'updated_at', 'nickname', 'like_count', 'is_liked'
        ]

    def get_like_count(self, obj):
        # 좋아요 개수 반환 (like_users 관계를 사용)
        return obj.like_users.count()

    def get_is_liked(self, obj):
        # 현재 요청한 사용자가 좋아요를 눌렀는지 여부
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__' 