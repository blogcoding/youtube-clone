from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from taggit.models import Tag
from channels.models import Subscription
from .forms import CommentCreateForm


def VideoDetailView(request, slug):
    video = Video.objects.get(slug=slug)
    recommendations = Video.objects.exclude(slug=video.slug)

    video.views += 1
    video.save()

    # similiar_videos = []
    # video_tags = []
    # for tag in video.tags.all():
    #     video_tags.append(tag)
    #     print(video_tags)
    # similiar_videos_by_tags = Video.objects.filter(tags__in=video_tags)
    # similiar_videos.append(similiar_videos_by_tags)
    # print(similiar_videos)

    context = {
        'video': video,
        'recommendations': recommendations,
        'sidebar_hidden': True,
    }

    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, channel=video.channel).count() == 0:
            context['subscribed'] = False
        else:
            context['subscribed'] = True

        if request.user in video.likes.all():
            context['liked'] = True

        if request.user in video.dislikes.all():
            context['disliked'] = True

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.channel = request.user.channel
            comment.video = video
            comment.save()
    else:
        form = CommentCreateForm()

    context['form'] = form

    return render(request, 'videos/detail.html', context)


def LikeVideo(request, slug):
    video = Video.objects.get(slug=slug)
    context = {}
    if request.user in video.likes.all():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)
        if request.user in video.dislikes.all():
            video.dislikes.remove(request.user)
            context['dislikes_count'] = video.dislikes.count()

    context['likes_count'] = video.likes.count()

    return JsonResponse(context)


def DislikeVideo(request, slug):
    video = Video.objects.get(slug=slug)
    context = {}

    if request.user in video.dislikes.all():
        video.dislikes.remove(request.user)
    else:
        video.dislikes.add(request.user)
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            context['likes_count'] = video.likes.count()

    context['dislikes_count'] = video.dislikes.count()

    return JsonResponse(context)


def CategoryDetailView(request, slug):
    category = Category.objects.get(slug=slug)
    videos = Video.objects.filter(category=category)

    context = {
        'videos': videos,
        'chips': True,
        "category_list": Category.objects.all(),
        'active_chip': category.slug
    }

    return render(request, 'core/category_detail.html', context)


def TagDetailView(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    videos = Video.objects.filter(tags__in=[tag])

    context = {
        'videos': videos,
        'tag': tag,
        'videos_count': videos.count()
    }

    return render(request, 'core/tag_detail.html', context)
