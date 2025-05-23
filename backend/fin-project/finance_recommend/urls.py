from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_prd, name="prd_api_call"),
    ]
