from django.urls import path
from .views import *
from videos.views import CategoryDetailView, TagDetailView
from channels.views import ChannelsListView


urlpatterns = [
    path('', index, name='homepage'),
    path('hashtag/<str:slug>', TagDetailView, name='tag-detail'),
    path('category/<str:slug>', CategoryDetailView, name='category-detail'),
    path('feed/subscriptions', subscriptions, name='subscriptions'),
    path('feed/channels', ChannelsListView, name='channels-list'),
    path('feed/library', LibraryView, name='library')
]
