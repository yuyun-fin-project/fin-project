from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
# 권한 별 접근 관리
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# get, post 함수 나누기
@api_view(['GET', 'POST'])
def article_get_or_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({
            "count": articles.count(),
            "results": serializer.data,
        })
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied("로그인이 필요합니다.")
        serializer = ArticleSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    # 작성자 권한 체크
    if request.user != article.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        data = {
            'delete': f'등록 번호 {article_pk} 번의 {article.title}을 삭제하였습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

# 조건 별로 검색하는 함수 (query 기반)
@api_view(['GET'])
def article_search(request):
    query_param = request.query_params.get('is_group', False)
    if query_param:
        if query_param == 'True' or query_param == 'true':
            articles = Article.objects.filter(is_group=True)
        else:
            articles = Article.objects.filter(is_group=False)
    else:
        articles = Article.objects.all()
    
    serializer = ArticleSerializer(artists, many=True)


@api_view()
def stats(request):
       # 오늘 날짜 계산
    today = timezone.now().date()
    
    # 전체 게시글 수
    total_posts = Article.objects.count()
    
    # 전체 사용자 수
    User = get_user_model()
    total_users = User.objects.count()
    
    # 오늘 작성된 게시글 수
    today_posts = Article.objects.filter(created_at__date=today).count()
    
    # 전체 댓글 수
    total_comments = Comment.objects.count()
    
    # 응답 데이터 구성
    data = {
        'total_posts': str(total_posts),
        'total_users': str(total_users),
        'today_posts': str(today_posts),
        'total_comments': str(total_comments),
    }
    print(data)
    return Response(data)


@api_view()
def recent_articles(request):
    recent_posts = Article.objects.annotate(
        like_count=Count('like_users')
    ).order_by('-like_count', '-created_at')[:2]
    
    serializer = ArticleSerializer(recent_posts, many=True)
    print(serializer.data)
    return Response({
        'recent_articles': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        liked = False
    else:
        article.like_users.add(request.user)
        liked = True
    return Response({
            "liked": liked,
            "like_count": article.like_users.count()
        }, status=status.HTTP_200_OK)