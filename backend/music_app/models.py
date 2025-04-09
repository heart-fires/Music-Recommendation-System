from django.db import models

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