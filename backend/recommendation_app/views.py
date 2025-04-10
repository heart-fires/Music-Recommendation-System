# recommendation_app/views.py
import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserAction
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from music_app.models import Song
from collections import defaultdict
import math
import json
from .models import RecommendationFeedback

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_action_weights(self, user):
        action_weights = defaultdict(int)
        user_actions = UserAction.objects.filter(user=user)
        for action in user_actions:
            if action.action_type == 'play':
                action_weights[action.song.song_name] += 1
            elif action.action_type == 'collect':
                action_weights[action.song.song_name] += 3
            elif action.action_type == 'like':
                action_weights[action.song.song_name] += 2
            elif action.action_type == 'share':
                action_weights[action.song.song_name] += 2
        return action_weights

    def get_similarity(self, user1, user2):
        user1_weights = self.get_user_action_weights(user1)
        user2_weights = self.get_user_action_weights(user2)
        common_songs = set(user1_weights.keys()) & set(user2_weights.keys())
        numerator = sum([user1_weights[song] * user2_weights[song] for song in common_songs])
        denominator1 = math.sqrt(sum([weight ** 2 for weight in user1_weights.values()]))
        denominator2 = math.sqrt(sum([weight ** 2 for weight in user2_weights.values()]))
        if denominator1 == 0 or denominator2 == 0:
            return 0
        return numerator / (denominator1 * denominator2)

    def get_similar_users(self, target_user, k):
        all_users = User.objects.exclude(id=target_user.id)
        user_similarities = []
        for user in all_users:
            similarity = self.get_similarity(target_user, user)
            user_similarities.append((user, similarity))
        user_similarities.sort(key=lambda x: x[1], reverse=True)
        return user_similarities[:k]

    def get_recommended_songs(self, target_user, similar_users):
        target_user_songs = set(UserAction.objects.filter(user=target_user).values_list('song__song_name', flat=True))
        recommended_songs = []
        for user, _ in similar_users:
            user_songs = UserAction.objects.filter(user=user).values_list('song__song_name', flat=True)
            for song_name in user_songs:
                if song_name not in target_user_songs:
                    try:
                        song = Song.objects.get(song_name=song_name)
                        recommended_songs.append({
                            'song_name': song.song_name,
                            'singer': song.singer,
                            'category': song.category
                        })
                        target_user_songs.add(song_name)
                    except Song.DoesNotExist:
                        continue
        return recommended_songs

    def get(self, request):
        target_user = request.user
        cache_key = f'recommendations:{target_user.id}'
        cached_recommendations = redis_client.get(cache_key)
        if cached_recommendations:
            recommended_songs = json.loads(cached_recommendations)
        else:
            k = 5  # 选择最相似的 5 个用户
            similar_users = self.get_similar_users(target_user, k)
            recommended_songs = self.get_recommended_songs(target_user, similar_users)
            redis_client.set(cache_key, json.dumps(recommended_songs), ex=3600)  # 缓存 1 小时
        return Response(recommended_songs, status=status.HTTP_200_OK)

# 在 backend/recommendation_app/views.py 中添加反馈接口
class RecommendationFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target_user = request.user
        song_name = request.data.get('song_name')
        feedback = request.data.get('feedback')

        # 记录反馈数据
        RecommendationFeedback.objects.create(user=target_user, song_name=song_name, feedback=feedback)

        return Response({'message': '反馈记录成功'}, status=status.HTTP_200_OK)