from django.urls import path
from . import views

app_name='articles'

urlpatterns = [
    # 해당 API는 메소드에 따라 조회 생성
    path('', views.article_get_or_create, name='article_get_or_create' ),
    # 해당 API는 메소드에 따라 수정/삭제/상세조회
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
]
