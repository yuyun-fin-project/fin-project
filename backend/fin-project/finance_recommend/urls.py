from django.urls import path
from . import views

urlpatterns = [
    path("spot/", views.get_spot, name="spot_api"),
    path("spot/<start_date>/<end_date>/", views.get_spot, name="spot_api"),
    path('bookmark/product/<int:product_id>/', views.product_bookmark, name="product_bookmark"),
    path('bookmark/product/', views.product_bookmark_list, name="product_bookmarks"),
    path('bookmark/spot/<int:spot_product_id>/', views.spot_bookmark, name="spot_bookmark"),
    path('bookmark/spot/', views.spot_bookmark_list, name="spot_bookmarks"),
    path('', views.get_prd, name="prd_api"),
    path('recommend/', views.recommend_view, name="recommend_view"),
    path('recommend/queries/', views.get_recommendation_queries, name="recommendation_queries"),
]