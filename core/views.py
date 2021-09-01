from django.shortcuts import render
from videos.models import Video, Category
from channels.models import Channel, Subscription
from playlists.models import Playlist


def index(request):
    context = {
        'videos': Video.objects.all(),
        'chips': True,
        "category_list": Category.objects.all(),
        'active_chip': 'all'
    }

    return render(request, 'core/index.html', context)


def subscriptions(request):
    context = {}

    if request.user.is_authenticated:
        # if request.user.channel:
        #     videos = Video.objects.exclude(channel=request.user.channel)
        # else:
        #     videos = Video.objects.all()

        videos = []
        user_subscriptions = Subscription.objects.filter(user=request.user)

        for subscription in user_subscriptions:
            channel = subscription.channel
            # owner = channel.user
            videos.extend(list(Video.objects.filter(channel=channel)))

        context['videos'] = videos

    # try:
    #     channel = Channel.objects.filter(user__username=request.user).get().channel_name != ""
    #     print(channel)
    #     context['channel'] = channel
    # except Channel.DoesNotExist:
    #     channel = False

    return render(request, "core/subscriptions.html", context)


def LibraryView(request):
    context = {}

    if request.user.is_authenticated:
        liked = Playlist.objects.get(user=request.user, slug='liked').videos.all()[:5]
        liked_count = Playlist.objects.get(user=request.user, slug='liked').videos.all().count()
        context['liked_count'] = liked_count
        context['liked_videos'] = liked
        later = Playlist.objects.get(user=request.user, slug='later').videos.all()[:5]
        later_count = Playlist.objects.get(user=request.user, slug='later').videos.all().count()
        context['later_videos'] = later
        context['later_count'] = later_count
        playlists = Playlist.objects.filter(user=request.user).exclude(slug='later').exclude(slug='liked')[:10]
        context['playlists'] = playlists

    return render(request, 'core/library.html', context)
