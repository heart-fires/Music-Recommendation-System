import { createRouter, createWebHistory } from 'vue-router';
import RegisterView from '../views/RegisterView.vue';
import LoginView from '../views/LoginView.vue';
import UserProfileView from '../views/UserProfileView.vue';
import SongList from '../views/SongList.vue';
import PlaylistManager from '../views/PlaylistManager.vue';
import SongDetail from '../views/SongDetail.vue';
import WechatLoginView from '../views/WechatLoginView.vue';

const routes = [
  {
    path: '/wechat/login',
    name: 'WechatLogin',
    component: WechatLoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/songs',
    name: 'SongList',
    component: SongList
  },
  {
    path: '/playlists',
    name: 'PlaylistManager',
    component: PlaylistManager
  },
  {
    path: '/songs/:song_name',
    name: 'SongDetail',
    component: SongDetail
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    next('/login');
  } else {
    next();
  }
});

export default router;    