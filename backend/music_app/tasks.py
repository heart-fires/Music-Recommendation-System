# backend/music_app/tasks.py
from .models import Song
from .music_api import get_music_list

def update_music_library():
    music_list = get_music_list()
    for music in music_list:
        song_name = music.get('song_name')
        singer = music.get('singer')
        category = music.get('category')
        lyrics = music.get('lyrics')

        if not Song.objects.filter(song_name=song_name).exists():
            song = Song(song_name=song_name, singer=singer, category=category, lyrics=lyrics)
            song.save()