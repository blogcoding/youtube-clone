from django.db import models
from django.contrib.auth import get_user_model
from videos.models import Video
from channels.utils import get_random_slug
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


PRIVATE_CHOICES = (
    ('private', 'Для себя'),
    ('public', 'Для всех'),
    ('link', 'По ссылке')
)


class Playlist(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название плейлиста')
    slug = models.SlugField(max_length=50, blank=True, null=True)
    private = models.CharField(max_length=15, default='private', verbose_name='Конфиденциальность', choices=PRIVATE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', verbose_name='Пользователь')
    videos = models.ManyToManyField(Video, verbose_name='Видео', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        ex = False
        if not self.slug:
            to_slug = slugify(get_random_slug())

            ex = Playlist.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(get_random_slug())
                ex = Playlist.objects.filter(slug=to_slug).exists()

            self.slug = to_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'


@receiver(post_save, sender=User)
def post_save_create_liked(sender, instance, created, **kwargs):
    if created:
        Playlist.objects.create(user=instance, title='Понравившиеся', slug='liked', private='private')


@receiver(post_save, sender=User)
def post_save_create_later(sender, instance, created, **kwargs):
    if created:
        Playlist.objects.create(user=instance, title='Смотреть позже', slug='later', private='private')
