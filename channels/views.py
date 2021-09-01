from django.shortcuts import render, redirect
from .models import Channel, Subscription
from playlists.models import Playlist
from videos.models import Video


def ChannelDetailView(request, slug):
    channel = Channel.objects.get(slug=slug)

    context = {
        'channel': channel,
        'activeTab': 'featured'
    }

    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

    return render(request, 'channels/featured.html', context)


def ChannelVideosView(request, slug):
    channel = Channel.objects.get(slug=slug)
    videos = Video.objects.filter(channel=channel)

    context = {
        'channel': channel,
        'activeTab': 'videos',
        'videos': videos
    }
    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

    return render(request, 'channels/videos.html', context)


def ChannelPlaylistsView(request, slug):
    channel = Channel.objects.get(slug=slug)
    playlists = Playlist.objects.filter(user=channel.user, private='public')

    context = {
        'channel': channel,
        'activeTab': 'playlists',
        'playlists': playlists
    }
    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

    return render(request, 'channels/playlists.html', context)


def ChannelCommunityView(request, slug):
    channel = Channel.objects.get(slug=slug)

    context = {
        'channel': channel,
        'activeTab': 'community'
    }
    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

    return render(request, 'channels/community.html', context)


def ChannelChannelsView(request, slug):
    channel = Channel.objects.get(slug=slug)

    context = {
        'channel': channel,
        'activeTab': 'channels'
    }
    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

    return render(request, 'channels/channels.html', context)


def ChannelAboutView(request, slug):
    channel = Channel.objects.get(slug=slug)

    context = {
        'channel': channel,
        'activeTab': 'about'
    }
    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

    return render(request, 'channels/about.html', context)


def ChannelsListView(request):
    if request.user.is_authenticated:
        user_subscriptions = Subscription.objects.filter(user=request.user)
        context = {
            'subscriptions': user_subscriptions
        }
        return render(request, 'core/channels_list.html', context)
    else:
        return redirect('account_login')

# TODO: редирект на логин


def ChannelSubscribe(request, channel_slug):
    channel = Channel.objects.get(slug=channel_slug)
    new_subscription = Subscription(user=request.user, channel=channel)
    new_subscription.save()

    channel.subscribers += 1

    channel.save()

    return redirect(request.META['HTTP_REFERER'])


def channelUnsubscribe(request, channel_slug):
    channel = Channel.objects.get(slug=channel_slug)
    subscription = Subscription.objects.get(user=request.user, channel=channel)
    subscription.delete()

    channel.subscribers -= 1

    channel.save()

    return redirect(request.META['HTTP_REFERER'])
