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

const audioRef = ref(null);
const currentSong = ref(props.initialSong);
const isPlaying = ref(false);
const currentTime = ref(0);
const totalDuration = ref(0);
const lyrics = ref([]);
const currentPlaylist = ref(props.playlist);
const currentIndex = ref(0);

onMounted(async () => {
  if (currentSong.value.song_name) {
    await loadSong(currentSong.value);
  }
});

const loadSong = async (song) => {
  try {
    const response = await axios.get(`/music/play/${song.song_name}/`);
    audioRef.value.src = response.data.music_url;
    audioRef.value.load();
    audioRef.value.play();
    isPlaying.value = true;

    const lyricsResponse = await axios.get(`/music/lyrics/${song.song_name}/`);
    lyrics.value = parseLyrics(lyricsResponse.data.lyrics);

    audioRef.value.addEventListener('timeupdate', () => {
      currentTime.value = audioRef.value.currentTime;
    });

    audioRef.value.addEventListener('ended', () => {
      nextSong();
    });

    audioRef.value.addEventListener('loadedmetadata', () => {
      totalDuration.value = audioRef.value.duration;
    });
  } catch (error) {
    console.error('加载歌曲失败:', error);
  }
};

const togglePlay = () => {
  if (isPlaying.value) {
    audioRef.value.pause();
  } else {
    audioRef.value.play();
  }
  isPlaying.value = !isPlaying.value;
};

const prevSong = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    currentSong.value = currentPlaylist.value[currentIndex.value];
    loadSong(currentSong.value);
  }
};

const nextSong = () => {
  if (currentIndex.value < currentPlaylist.value.length - 1) {
    currentIndex.value++;
    currentSong.value = currentPlaylist.value[currentIndex.value];
    loadSong(currentSong.value);
  }
};

const seek = (time) => {
  audioRef.value.currentTime = time;
};

const formatTime = (time) => {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60);
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
};

const parseLyrics = (lyricsText) => {
  const lines = lyricsText.split('\n');
  return lines.map((line) => {
    const timeMatch = line.match(/\[(\d{2}):(\d{2})\.(\d{2})\]/);
    if (timeMatch) {
      const minutes = parseInt(timeMatch[1]);
      const seconds = parseInt(timeMatch[2]);
      const ms = parseInt(timeMatch[3]);
      const time = minutes * 60 + seconds + ms / 100;
      const text = line.replace(/\[.*?\]/, '').trim();
      return { time, text };
    }
    return { time: 0, text: line };
  });
};

const isActiveLyric = (lyricTime) => {
  return lyricTime <= currentTime.value && (lyrics.value[lyrics.value.findIndex((l) => l.time === lyricTime) + 1]?.time > currentTime.value || true);
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