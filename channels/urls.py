from django.urls import path
from .views import *

urlpatterns = [
    path('subscribe/<str:channel_slug>', ChannelSubscribe, name='channel-subscribe'),
    path('unsubscribe/<str:channel_slug>', channelUnsubscribe, name='channel-unsubscribe'),
    path('<str:slug>/featured', ChannelDetailView, name='channel-detail'),
    path('<str:slug>/videos', ChannelVideosView, name='channel-videos'),
    path('<str:slug>/playlists', ChannelPlaylistsView, name='channel-playlists'),
    path('<str:slug>/community', ChannelCommunityView, name='channel-community'),
    path('<str:slug>/channels', ChannelChannelsView, name='channel-channels'),
    path('<str:slug>/about', ChannelAboutView, name='channel-about'),
]
