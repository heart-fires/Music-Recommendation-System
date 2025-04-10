from django.db import models
from user_app.models import User
from .models import Song

# 修改后
class Song(models.Model):
    song_name = models.CharField(max_length=50, primary_key=True)
    singer = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    music_type = models.CharField(max_length=20, choices=[('pure', '纯音乐'), ('non_pure', '非纯音乐')], null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.song_name

class SongComment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.id} - {self.song.song_name} - {self.text[:20]}"
        # 截取前20个字符作为评论预览