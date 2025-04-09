from django.db import models
from user_app.models import User
from music_app.models import Song

class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    action_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.id} - {self.song.song_name} - {self.action_type}"