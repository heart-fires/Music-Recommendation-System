<template>
  <div class="login-container">
    <el-form :model="form" ref="formRef" label-width="100px" status-icon>
      <el-form-item label="用户 ID" prop="id">
        <el-input v-model="form.id" placeholder="请输入用户 ID"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const formRef = ref(null);
const form = ref({
  id: '',
  password: ''
});
const router = useRouter();

const handleLogin = async () => {
  const valid = await new Promise((resolve) => {
    formRef.value.validate((valid) => {
      resolve(valid);
    });
  });

  if (!valid) {
    ElMessage.error('请填写完整且正确的信息');
    return;
  }

  try {
    const response = await axios.post('/user/login/', form.value);
    if (response.status === 200) {
      ElMessage.success('登录成功');
      localStorage.setItem('token', response.data.token);
      router.push('/');
    } else {
      ElMessage.error(response.data.message || '登录失败，请重试');
    }
  } catch (error) {
    ElMessage.error('登录失败，请稍后重试');
  }
};
</script>

<style scoped>
.login-container {
  padding: 20px;
  width: 300px;
  margin: 50px auto;
}
</style>