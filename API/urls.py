from django.urls import path
from API.views import *

urlpatterns = [
    path('summary/', ai_video_summary.as_view(), name='video_summary'),
]