from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
# 권한 별 접근 관리
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_get_or_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({
            "count": articles.count(),
            "results": serializer.data
        })
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
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
def artist_condition_list(request):
    query_param = request.query_params.get('is_group', False)
    if query_param:
        if query_param == 'True' or query_param == 'true':
            articles = Article.objects.filter(is_group=True)
        else:
            articles = Article.objects.filter(is_group=False)
    else:
        articles = Article.objects.all()
    
    serializer = ArticleSerializer(artists, many=True)
