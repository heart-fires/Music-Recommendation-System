from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user_app.views import WechatConfigView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_app.urls')),
    path('music/', include('music_app.urls')),
    path('recommend/', include('recommendation_app.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('wechat/config/', WechatConfigView.as_view(), name='wechat_config'),

]

