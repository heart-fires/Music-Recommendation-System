from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from rest_framework.permissions import IsAuthenticated
from .music_api import get_music_url
from recommendation_app.models import UserAction
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class Top10SongsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_admin:
            top_10_songs = UserAction.objects.values('song__song_name').annotate(play_count=Count('id')).order_by('-play_count')[:10]
            return Response(top_10_songs, status=status.HTTP_200_OK)
        return Response({'message': '只有管理员可以查看统计信息'}, status=status.HTTP_403_FORBIDDEN)

class CategoryPlayCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_admin:
            category_play_count = UserAction.objects.values('song__category').annotate(play_count=Count('id')).order_by('-play_count')
            return Response(category_play_count, status=status.HTTP_200_OK)
        return Response({'message': '只有管理员可以查看统计信息'}, status=status.HTTP_403_FORBIDDEN)

class SongReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, song_name):
        if request.user.is_admin:
            try:
                song = Song.objects.get(song_name=song_name)
                action = request.data.get('action')
                if action == 'approve':
                    song.is_online = True
                    song.save()
                    return Response({'message': '歌曲审核通过，已上线'}, status=status.HTTP_200_OK)
                elif action == 'reject':
                    song.is_online = False
                    song.save()
                    # 通知用户歌曲下线
                    # 这里可以添加具体的通知逻辑
                    return Response({'message': '歌曲审核未通过，已下线'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': '无效的操作'}, status=status.HTTP_400_BAD_REQUEST)
            except Song.DoesNotExist:
                return Response({'message': '歌曲未找到'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': '只有管理员可以进行审核操作'}, status=status.HTTP_403_FORBIDDEN)


class SongPlayView(APIView):
    def get(self, request, song_name):
        try:
            song = Song.objects.get(song_name=song_name)
            # 假设 song 模型中有 song_id 字段存储网易云音乐的歌曲 ID
            song_id = song.song_id
            music_url = get_music_url(song_id)
            if music_url:
                return Response({'music_url': music_url}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to get music URL'}, status=status.HTTP_404_NOT_FOUND)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

class SongUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        song_name = data.get('song_name')
        singer = data.get('singer')
        category = data.get('category')
        lyrics = data.get('lyrics')

        if Song.objects.filter(song_name=song_name).exists():
            return Response({'message': 'Song already exists'}, status=status.HTTP_400_BAD_REQUEST)

        song = Song(song_name=song_name, singer=singer, category=category, lyrics=lyrics)
        song.save()
        return Response({'message': 'Song uploaded successfully'}, status=status.HTTP_201_CREATED)

class SongSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'message': 'No query parameter provided'}, status=status.HTTP_400_BAD_REQUEST)

        year = request.query_params.get('year')
        category = request.query_params.get('category')
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)

        songs = Song.objects.all()
        if query:
            songs = songs.filter(song_name__icontains=query) | \
                    songs.filter(singer__icontains=query) | \
                    songs.filter(lyrics__icontains=query)
        if year:
            # 假设歌曲有发布年份字段
            songs = songs.filter(year=year)
        if category:
            songs = songs.filter(category=category)

        songs = songs.order_by('song_name')
        paginator = Paginator(songs, page_size)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        result = [{'song_name': song.song_name, 'singer': song.singer, 'category': song.category} for song in page_obj]
        return Response({
            'results': result,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number
        }, status=status.HTTP_200_OK)


class SongAdminView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_admin:
            songs = Song.objects.all()
            result = [{'song_name': song.song_name,'singer': song.singer, 'category': song.category, 'is_online': song.is_online} for song in songs]
            return Response(result, status=status.HTTP_200_OK)
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, song_name):
        if request.user.is_admin:
            try:
                song = Song.objects.get(song_name=song_name)
                data = request.data
                song.singer = data.get('singer', song.singer)
                song.category = data.get('category', song.category)
                song.is_online = data.get('is_online', song.is_online)
                song.save()
                return Response({'message': 'Song updated successfully'}, status=status.HTTP_200_OK)
            except Song.DoesNotExist:
                return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, song_name):
        if request.user.is_admin:
            try:
                song = Song.objects.get(song_name=song_name)
                song.delete()
                return Response({'message': 'Song deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Song.DoesNotExist:
                return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)