import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import App from './App.vue';
import router from './router';
import axios from 'axios';

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.config.globalProperties.$axios = axios;
app.mount('#app');    