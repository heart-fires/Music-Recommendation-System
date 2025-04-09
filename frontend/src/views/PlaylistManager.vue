<template>
  <div class="playlist-manager">
    <h2>播放列表管理</h2>
    <el-form :model="newPlaylist" ref="formRef" label-width="80px">
      <el-form-item label="名称">
        <el-input v-model="newPlaylist.name"></el-input>
      </el-form-item>
      <el-form-item label="是否公开">
        <el-switch v-model="newPlaylist.is_public"></el-switch>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="createPlaylist">创建</el-button>
      </el-form-item>
    </el-form>
    <el-list>
      <el-list-item v-for="playlist in playlists" :key="playlist.id">
        {{ playlist.name }} - {{ playlist.is_public ? '公开' : '私有' }}
        <el-button type="text" @click="deletePlaylist(playlist.id)">删除</el-button>
        <el-button type="text" @click="viewPlaylist(playlist.id)">查看</el-button>
      </el-list-item>
    </el-list>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const newPlaylist = ref({
  name: '',
  is_public: true
});
const playlists = ref([]);
const formRef = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get('/playlist/');
    playlists.value = response.data;
  } catch (error) {
    console.error('获取播放列表失败:', error);
  }
});

const createPlaylist = async () => {
  try {
    const response = await axios.post('/playlist/', newPlaylist.value);
    playlists.value.push(response.data);
    newPlaylist.value = {
      name: '',
      is_public: true
    };
    ElMessage.success('播放列表创建成功');
  } catch (error) {
    console.error('创建播放列表失败:', error);
    ElMessage.error('创建播放列表失败');
  }
};

const deletePlaylist = async (playlistId) => {
  try {
    await axios.delete(`/playlist/${playlistId}/`);
    playlists.value = playlists.value.filter((p) => p.id !== playlistId);
    ElMessage.success('播放列表删除成功');
  } catch (error) {
    console.error('删除播放列表失败:', error);
    ElMessage.error('删除播放列表失败');
  }
};

const viewPlaylist = (playlistId) => {
  // 可以在这里实现查看播放列表详情的逻辑
  console.log('查看播放列表:', playlistId);
};
</script>

<style scoped>
.playlist-manager {
  padding: 20px;
}
</style>