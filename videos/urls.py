from django.urls import path
from .views import *

urlpatterns = [
    path('watch/<str:slug>', VideoDetailView, name='video-detail'),
    path('like/<str:slug>', LikeVideo, name='like-video'),
    path('dislike/<str:slug>', DislikeVideo, name='dislike-video'),
]
