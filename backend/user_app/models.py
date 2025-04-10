from django.db import models

class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    favorite_type_of_music = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.id