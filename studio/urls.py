from django.urls import path
from .views import *


urlpatterns = [
    path('', StudioIndexView, name='studio-index'),
]
