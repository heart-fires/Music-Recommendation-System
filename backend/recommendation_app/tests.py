import os
import django
# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
# 初始化 Django 设置
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserAction
from music_app.models import Song
from .views import RecommendationView


class RecommendationViewTest(TestCase):
    def setUp(self):
        # 不手动指定 id
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.song1 = Song.objects.create(song_name='Song1', singer='Singer1', category='Pop')
        self.song2 = Song.objects.create(song_name='Song2', singer='Singer2', category='Rock')
        UserAction.objects.create(user=self.user1, song=self.song1, action_type='play')
        UserAction.objects.create(user=self.user2, song=self.song2, action_type='play')

    def test_recommendation_similarity(self):
        view = RecommendationView()
        # 假设 get_similarity 方法存在
        try:
            similarity = view.get_similarity(self.user1, self.user2)
            self.assertEqual(similarity, 0.0)  # 无共同歌曲时相似度为0
        except AttributeError:
            self.fail("RecommendationView 类中缺少 get_similarity 方法")