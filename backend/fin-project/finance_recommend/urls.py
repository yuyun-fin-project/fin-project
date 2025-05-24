from django.urls import path
from . import views

urlpatterns = [
    path("spot/", views.get_spot, name="spot_api"),
]