<template>
  <div class="profile-container">
    <el-card>
      <template #header>
        <div>个人中心</div>
      </template>
      <div class="profile-info">
        <p>用户 ID: {{ user.id }}</p>
        <p>手机号: {{ user.phone_number }}</p>
        <p>是否为管理员: {{ user.is_admin ? '是' : '否' }}</p>
        <p>喜欢的音乐类型: {{ user.favorite_type_of_music || '暂无' }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const user = ref({});

onMounted(async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    ElMessage.error('请先登录');
    return;
  }

  try {
    const response = await axios.get('/user/profile/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    user.value = response.data;
  } catch (error) {
    ElMessage.error('获取用户信息失败，请稍后重试');
  }
});
</script>

<style scoped>
.profile-container {
  padding: 20px;
  width: 300px;
  margin: 50px auto;
}

.profile-info {
  padding: 10px;
}
</style>    