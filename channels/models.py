from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from .utils import get_random_slug

User = get_user_model()


class Channel(models.Model):
    user = models.OneToOneField(User, related_name='channel', on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=50, verbose_name='Название канала', blank=True, null=True)
    slug = models.SlugField(verbose_name='URL канала', blank=True, null=True)
    banner = models.ImageField(upload_to='channels/banners/', verbose_name='Баннер канала', blank=True, null=True)
    avatar = models.ImageField(upload_to='channels/avatars/', verbose_name='Фото канала', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    subscribers = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            ex = False
            to_slug = self.slug

            if self.title:
                to_slug = slugify(self.title)
                ex = Channel.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(get_random_slug())
                    ex = Channel.objects.filter(slug=to_slug).exists()
            else:
                self.title = str(self.user.first_name) + " " + str(self.user.last_name)
                to_slug = slugify(str(self.user.first_name) + " " + str(self.user.last_name))
                ex = Channel.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(get_random_slug())
                    ex = Channel.objects.filter(slug=to_slug).exists()

            self.slug = to_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='subscription')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='Канал')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return '{} follows {}'.format(self.user, self.channel)
