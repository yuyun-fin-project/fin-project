# accounts/urls.py
from django.urls import path
from . import views
from django.urls import path
from .views import CookieTokenRefreshView


app_name = 'accounts'
urlpatterns = [
    # path('logout/', views.logout, name='logout'),
    # path('profile/<username>/', views.profile, name = 'profile'),
    path('google/login/', views.google_login, name='google-login'),
    path('google/callback/', views.google_callback, name='google-callback'),
    path('kakao/login/', views.kakao_login, name='kakao-login'),
    path('kakao/callback/', views.kakao_callback, name='kakao-callback'),
    path("api/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]
