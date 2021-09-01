from django.urls import path
from .views import *

urlpatterns = [
    path('liked', LikedVideos, name='liked-videos'),
    path('later', WatchLater, name='watch-later'),
    path('add/<str:video_slug>/<str:playlist_slug>/', addToPlaylist, name='add-to-playlist'),
    path('remove/<str:video_slug>/<str:playlist_slug>/', removeFromPlaylist, name='remove-from-playlist'),
    path('<str:slug>', playlistDetail, name='playlist-detail'),
]
