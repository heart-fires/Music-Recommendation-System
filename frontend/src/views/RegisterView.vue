<template>
  <div class="register-container">
    <el-form :model="form" ref="formRef" label-width="100px" status-icon>
      <el-form-item label="用户 ID" prop="id">
        <el-input v-model="form.id" placeholder="请输入用户 ID"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="手机号" prop="phone_number">
        <el-input v-model="form.phone_number" placeholder="请输入手机号"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
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
  password: '',
  phone_number: ''
});
const router = useRouter();

const handleRegister = async () => {
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
    const response = await axios.post('/user/register/', form.value);
    if (response.status === 201) {
      ElMessage.success('注册成功，请登录');
      router.push('/login');
    } else {
      ElMessage.error(response.data.message || '注册失败，请重试');
    }
  } catch (error) {
    ElMessage.error('注册失败，请稍后重试');
  }
};
</script>

<style scoped>
.register-container {
  padding: 20px;
  width: 300px;
  margin: 50px auto;
}
</style>