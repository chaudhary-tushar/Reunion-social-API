from django.urls import path
import uuid
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


urlpatterns = [
    path('', views.index, name='index'),
    path('api/authenticate/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/follow/<int:id>',views.Follow.as_view(),name='follow'),
    path('api/unfollow/<int:id>',views.UnFollow.as_view(),name='unfollow'),
    path('api/like/<uuid:id>',views.Like.as_view(),name='like'),
    path('api/unlike/<uuid:id>',views.Unlike.as_view(),name='unlike'),
    path('api/comment/<uuid:id>',views.Comment.as_view(),name='comment'),
    path('api/posts/',views.Postit.as_view(),name='post'),
    path('api/posts/<uuid:id>',views.Get_Post.as_view(),name='getdelete'),
    path('api/all_posts/',views.All_Post.as_view(),name='all-post'),
    path('api/user/',views.Get_user.as_view(),name='getuser'),
    
]