<template>
  <div class="song-detail">
    <h2>{{ song.song_name }}</h2>
    <p>歌手: {{ song.singer }}</p>
    <p>类别: {{ song.category }}</p>
    <div class="comments">
      <h3>评论</h3>
      <el-list>
        <el-list-item v-for="comment in comments" :key="comment.id">
          <p>{{ comment.user }}: {{ comment.text }}</p>
          <p>{{ comment.created_at }}</p>
        </el-list-item>
      </el-list>
      <el-form :model="newComment" ref="commentForm" label-width="80px">
        <el-form-item label="评论内容">
          <el-input v-model="newComment.text" type="textarea"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitComment">提交评论</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="actions">
      <el-button @click="likeSong">点赞</el-button>
      <el-button @click="collectSong">收藏</el-button>
      <el-button @click="shareToWechat">分享到微信</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useRoute } from 'vue-router';
import wx from 'weixin-js-sdk';

const route = useRoute();
const song = ref({});
const comments = ref([]);
const newComment = ref({
  text: ''
});
const commentForm = ref(null);

onMounted(async () => {
  try {
    const songResponse = await axios.get(`/music/admin/${route.params.song_name}/`);
    song.value = songResponse.data;

    const commentsResponse = await axios.get(`/music/comments/${route.params.song_name}/`);
    comments.value = commentsResponse.data;

    // 初始化微信分享配置
    await initWechatShare();
  } catch (error) {
    console.error('获取歌曲详情或评论失败:', error);
  }
});

const submitComment = async () => {
  try {
    const response = await axios.post(`/music/comments/${route.params.song_name}/`, newComment.value);
    comments.value.push(response.data);
    newComment.value.text = '';
    ElMessage.success('评论提交成功');
  } catch (error) {
    console.error('提交评论失败:', error);
    ElMessage.error('提交评论失败');
  }
};

const likeSong = () => {
  // 实现点赞逻辑
  console.log('点赞歌曲:', song.value.song_name);
};

const collectSong = () => {
  // 实现收藏逻辑
  console.log('收藏歌曲:', song.value.song_name);
};

const shareToWechat = () => {
  wx.updateAppMessageShareData({
    title: song.value.song_name,
    desc: `歌手: ${song.value.singer}`,
    link: window.location.href,
    imgUrl: 'https://dummyimage.com/800x600/ff0000/ffffff',
    success: function () {
      ElMessage.success('分享成功');
    },
    fail: function (err) {
      ElMessage.error('分享失败: ' + err.errMsg);
    }
  });
};

const initWechatShare = async () => {
  try {
    const response = await axios.get('/wechat/jsapi_config/', {
      params: {
        url: window.location.href
      }
    });
    const config = response.data;
    wx.config({
      debug: false,
      appId: config.appId,
      timestamp: config.timestamp,
      nonceStr: config.nonceStr,
      signature: config.signature,
      jsApiList: ['updateAppMessageShareData']
    });
    wx.ready(() => {
      shareToWechat();
    });
    wx.error((res) => {
      console.error('微信配置失败:', res.errMsg);
    });
  } catch (error) {
    console.error('获取微信 JSAPI 配置失败:', error);
  }
};
</script>

<style scoped>
.song-detail {
  padding: 20px;
}

.comments {
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
}
</style>