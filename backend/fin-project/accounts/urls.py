from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('logout/', views.logout, name='logout'),
    # path('profile/<username>/', views.profile, name = 'profile'),
    path('google/login/', views.google_login, name='google-login'),
    path('google/callback/', views.google_callback, name='google-callback'),
]
