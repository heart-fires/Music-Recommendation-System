from django.urls import path
from .views import (SongUploadView, SongSearchView, SongAdminView, SongPlayView,
                    SongReviewView, CategoryPlayCountView, Top10SongsView)

urlpatterns = [
    path('upload/', SongUploadView.as_view(), name='song-upload'),
    path('search/', SongSearchView.as_view(), name='song-search'),
    path('admin/<str:song_name>/', SongAdminView.as_view(), name='song-admin'),
    path('play/<str:song_name>/', SongPlayView.as_view(), name='song-play'),
    path('review/<str:song_name>/', SongReviewView.as_view(), name='song-review'),
    path('category-play-count/', CategoryPlayCountView.as_view(), name='category-play-count'),
    path('top-10-songs/', Top10SongsView.as_view(), name='top-10-songs'),
]

