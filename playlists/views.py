from django.shortcuts import render, redirect
from .models import Playlist
from videos.models import Video


def playlistDetail(request, slug):

    playlist = Playlist.objects.get(slug=slug)

    context = {
        'playlist': playlist
    }

    return render(request, 'playlists/detail.html', context)


def LikedVideos(request):
    context = {}
    if request.user.is_authenticated:
        liked = Playlist.objects.get(user=request.user, slug='liked')
        context['playlist'] = liked

    return render(request, 'playlists/liked.html', context)


def WatchLater(request):
    context = {}
    if request.user.is_authenticated:
        later = Playlist.objects.get(user=request.user, slug='later')
        context['playlist'] = later

    return render(request, 'playlists/later.html', context)


def addToPlaylist(request, playlist_slug, video_slug):
    if request.user.is_authenticated:
        playlist = Playlist.objects.get(user=request.user, slug=playlist_slug)
        video = Video.objects.get(slug=video_slug)
        playlist.videos.add(video)

    return redirect(request.META['HTTP_REFERER'])


def removeFromPlaylist(request, playlist_slug, video_slug):
    if request.user.is_authenticated:
        playlist = Playlist.objects.get(user=request.user, slug=playlist_slug)
        video = Video.objects.get(slug=video_slug)
        playlist.videos.remove(video)

    return redirect(request.META['HTTP_REFERER'])