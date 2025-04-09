<template>
  <div class="music-player">
    <div class="player-info">
      <h3>{{ currentSong.song_name }}</h3>
      <p>{{ currentSong.singer }}</p>
    </div>
    <div class="player-controls">
      <el-button @click="prevSong" icon="el-icon-arrow-left"></el-button>
      <el-button @click="togglePlay" :icon="isPlaying ? 'el-icon-pause' : 'el-icon-play'"></el-button>
      <el-button @click="nextSong" icon="el-icon-arrow-right"></el-button>
    </div>
    <div class="progress-container">
      <el-slider
        v-model="currentTime"
        :max="totalDuration"
        @input="seek"
        show-input
        input-size="small"
      ></el-slider>
      <div class="time-display">
        {{ formatTime(currentTime) }} / {{ formatTime(totalDuration) }}
      </div>
    </div>
    <div class="lyrics-container" v-if="lyrics.length > 0">
      <div
        v-for="(line, index) in lyrics"
        :key="index"
        :class="{ 'active-lyric': isActiveLyric(line.time) }"
      >
        {{ line.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps({
  initialSong: {
    type: Object,
    default: () => ({})
  },
  playlist: {
    type: Array,
    default: () => []
  }
});

const currentSong = ref(props.initialSong);
const isPlaying = ref(false);
const currentTime = ref(0);
const lyrics = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get(`/music/lyrics/${currentSong.value.song_name}/`);
    lyrics.value = response.data;
  } catch (error) {
    console.error('获取歌词失败:', error);
  }
});

const isActiveLyric = (time) => {
  return currentTime.value >= time;
};
</script>

<style scoped>
.music-player {
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin: 20px auto;
  width: 600px;
}

.player-info {
  text-align: center;
  margin-bottom: 10px;
}

.player-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
}

.progress-container {
  margin-bottom: 10px;
}

.lyrics-container {
  height: 200px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  padding: 10px;
  border-radius: 4px;
}

.active-lyric {
  color: #409eff;
  font-weight: bold;
}
</style>