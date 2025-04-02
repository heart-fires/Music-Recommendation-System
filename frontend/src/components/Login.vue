<template>
  <div>
    <h1>登录</h1>
    <input v-model="username" placeholder="用户名" />
    <input v-model="password" placeholder="密码" type="password" />
    <button @click="login">登录</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          username: this.username,
          password: this.password
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>