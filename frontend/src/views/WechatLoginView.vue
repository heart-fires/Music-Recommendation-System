<template>
  <div>
    <el-button @click="redirectToWechatLogin">微信登录</el-button>
  </div>
</template>

<script setup>

// 这里需要替换为你自己的微信开放平台的 APPID 和回调地址
const APPID = 'your_appid';
const REDIRECT_URI = encodeURIComponent('http://yourdomain.com/wechat/callback');
const SCOPE = 'snsapi_userinfo';

const redirectToWechatLogin = () => {
  const wechatLoginUrl = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${APPID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=${SCOPE}&state=STATE#wechat_redirect`;
  window.location.href = wechatLoginUrl;
};
</script>

<style scoped>

</style>