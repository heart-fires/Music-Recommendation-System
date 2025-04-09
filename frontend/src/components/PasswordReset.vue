<template>
  <div>
    <h1>密码找回</h1>
    <input v-model="email" placeholder="邮箱" />
    <button @click="resetPassword">发送重置链接</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: ''
    };
  },
  methods: {
    async resetPassword() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/password-reset/', {
          email: this.email
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>