from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView, PaymentView, PasswordResetView, PasswordResetConfirmView
from .views import WechatCallbackView
from .views import UserDeleteView
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('password_reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('wechat/callback/', WechatCallbackView.as_view(), name='wechat-callback'),
    path('delete/<str:user_id>/', UserDeleteView.as_view(), name='user-delete'),
]