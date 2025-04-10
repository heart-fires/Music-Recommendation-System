<template>
  <div>
    <el-button @click="redirectToWechatLogin">微信登录</el-button>
  </div>
</template>

<script setup>
import axios from 'axios';

const getWechatConfig = async () => {
  try {
    const response = await axios.get('/wechat/config/');
    return response.data;
  } catch (error) {
    console.error('获取微信配置失败:', error);
    return {};
  }
};

const redirectToWechatLogin = async () => {
  const { APPID, REDIRECT_URI, SCOPE } = await getWechatConfig();
  const wechatLoginUrl = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${APPID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=${SCOPE}&state=STATE#wechat_redirect`;
  window.location.href = wechatLoginUrl;
};
</script>

<style scoped>

</style>