from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'singer', 'category', 'is_online')
    list_filter = ('category', 'is_online')
    search_fields = ('song_name', 'singer')
    actions = ['make_online', 'make_offline']

    def make_online(self, request, queryset):
        queryset.update(is_online=True)
    make_online.short_description = "上线选中的歌曲"

    def make_offline(self, request, queryset):
        queryset.update(is_online=False)
    make_offline.short_description = "下线选中的歌曲"

admin.site.register(Song, SongAdmin)