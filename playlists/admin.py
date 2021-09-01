from django.contrib import admin
from .models import *


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass

