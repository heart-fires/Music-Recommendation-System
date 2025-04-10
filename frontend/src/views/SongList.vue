<template>
  <div class="song-list">
    <h2>歌曲列表</h2>
    <el-list>
      <el-list-item
        v-for="song in songs"
        :key="song.song_name"
        @click="playSong(song)"
      >
        {{ song.song_name }} - {{ song.singer }}
        <el-button
          type="text"
          @click="addToPlaylist(song); $event.stopPropagation()"
        >
          添加到播放列表
        </el-button>
      </el-list-item>
    </el-list>
    <music-player :initial-song="currentSong" :playlist="playlist"></music-player>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import MusicPlayer from '../components/MusicPlayer.vue';

const songs = ref([]);
const currentSong = ref({});
const playlist = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get('/music/search/?q=');
    songs.value = response.data;
  } catch (error) {
    console.error('获取歌曲列表失败:', error);
  }
});

const playSong = (song) => {
  currentSong.value = song;
  if (!playlist.value.some((s) => s.song_name === song.song_name)) {
    playlist.value.push(song);
  }
};

const addToPlaylist = (song) => {
  if (!playlist.value.some((s) => s.song_name === song.song_name)) {
    playlist.value.push(song);
  }
};
</script>

<style scoped>
.song-list {
  padding: 20px;
}
</style>