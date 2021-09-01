from django.db import models
from channels.models import Channel
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from channels.utils import get_random_slug
from taggit.managers import TaggableManager


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории', unique=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Video(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок видео')
    slug = models.SlugField(max_length=50, blank=True, null=True, verbose_name='Слаг')
    channel = models.ForeignKey(Channel, related_name='videos', on_delete=models.CASCADE, verbose_name='Канал')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория',
                                 related_name='videos')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    tags = TaggableManager()
    preview = models.ImageField(upload_to='videos/previews/', verbose_name='Превью', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    video = models.FileField(upload_to='videos/videos/', verbose_name='Видео')

    likes = models.ManyToManyField(User, related_name='likes', verbose_name='Лайки', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', verbose_name='Дизлайки', blank=True)

    @property
    def get_likes_count(self):
        return self.likes.count()

    @property
    def get_dislikes_count(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            ex = False
            to_slug = slugify(get_random_slug())

            ex = Video.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(get_random_slug())
                ex = Video.objects.filter(slug=to_slug).exists()

            self.slug = to_slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ('-created',)


class Video_View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Видео')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    class Meta:
        verbose_name = 'Просмотр видео'
        verbose_name_plural = 'Просмотры видео'

# Моя реализация тегов - не работает сохранение поля manytomany, вариант решения который я нашел не оптимизирован
#
# hashtags_list = models.CharField(max_length=500, verbose_name='Список хэштегов', blank=True, null=True)
# hashtags = models.ManyToManyField(Hashtag, verbose_name='Хэштеги', null=True, blank=True, related_name='videos')
#
# class Hashtag(models.Model):
#     title = models.CharField(max_length=150, verbose_name='Заголовок хэштега')
#     slug = models.SlugField(max_length=170, blank=True, null=True, unique=True)
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = 'Хэштег'
#         verbose_name_plural = 'Хэштеги'
#
# if self.hashtags_list:
#     hashtags = self.hashtags_list
#     hashtags = hashtags.split(',')
#     print(hashtags)
#     for hashtag in hashtags:
#         new_hashtag, created = Hashtag.objects.get_or_create(title=hashtag, slug=slugify(hashtag))
#         self.hashtags.add(new_hashtag)
#         print(self.hashtags)


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    channel = models.ForeignKey(Channel, related_name='comments', on_delete=models.CASCADE, verbose_name='Канал')
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE, verbose_name='Видео')

    def __str__(self):
        return self.channel.title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created', )
