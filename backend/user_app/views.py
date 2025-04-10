import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.permissions import IsAuthenticated
from .payment_api import create_alipay_order
import uuid
import random
import redis
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest
from rest_framework.permissions import IsAdminUser


# 这里需要替换为你自己的阿里云短信服务配置
ACCESS_KEY_ID = 'your_access_key_id'
ACCESS_KEY_SECRET = 'your_access_key_secret'
SIGN_NAME = 'your_sign_name'
TEMPLATE_CODE = 'your_template_code'
# 从环境变量中获取配置信息
APPID = os.getenv('WECHAT_APPID')
APPSECRET = os.getenv('WECHAT_APPSECRET')
redis_client = redis.Redis(host='localhost', port=6379, db=0)


# 管理员删除用户信息
class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'message': '用户删除成功'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': '用户未找到'}, status=status.HTTP_404_NOT_FOUND)
# 微信开发者平台API获取
class WechatCallbackView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少授权码'}, status=status.HTTP_400_BAD_REQUEST)

        # 使用授权码换取 access_token 和 openid
        url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret={APPSECRET}&code={code}&grant_type=authorization_code'
        try:
            response = requests.get(url)
            data = response.json()
            if 'errcode' in data:
                return Response({'message': f'微信授权失败: {data["errmsg"]}'}, status=status.HTTP_400_BAD_REQUEST)
            access_token = data['access_token']
            openid = data['openid']

            # 使用 access_token 和 openid 获取用户信息
            user_info_url = f'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'
            user_info_response = requests.get(user_info_url)
            user_info = user_info_response.json()
            if 'errcode' in user_info:
                return Response({'message': f'获取用户信息失败: {user_info["errmsg"]}'},
                                status=status.HTTP_400_BAD_REQUEST)

            # 这里可以根据用户的 openid 进行用户的创建或登录操作
            # 示例：查找或创建用户
            user, created = User.objects.get_or_create(id=openid)
            if created:
                # 可以在这里设置用户的其他信息，如昵称、头像等
                user.nickname = user_info.get('nickname')
                user.avatar = user_info.get('headimgurl')
                user.save()

            return Response({'message': '微信登录成功', 'user_id': user.id}, status=status.HTTP_200_OK)
        except requests.RequestException:
            return Response({'message': '网络请求失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetView(APIView):
    def post(self, request):
        data = request.data
        phone_number = data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            # 生成验证码
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            # 存储验证码到 Redis，有效期 5 分钟
            redis_client.set(phone_number, code, ex=300)

            # 发送短信验证码
            client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-hangzhou')
            request = SendSmsRequest()
            request.set_accept_format('json')
            request.set_phone_numbers(phone_number)
            request.set_sign_name(SIGN_NAME)
            request.set_template_code(TEMPLATE_CODE)
            request.set_template_param({"code": code})
            response = client.do_action_with_exception(request)

            return Response({'message': '验证码已发送，请查收'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '该手机号未注册'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        data = request.data
        phone_number = data.get('phone_number')
        code = data.get('code')
        new_password = data.get('new_password')
        stored_code = redis_client.get(phone_number)
        if stored_code and stored_code.decode('utf-8') == code:
            try:
                user = User.objects.get(phone_number=phone_number)
                user.password = new_password
                user.save()
                redis_client.delete(phone_number)
                return Response({'message': '密码重置成功'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': '该手机号未注册'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': '验证码无效或已过期'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        total_amount = data.get('total_amount')
        subject = data.get('subject')
        out_trade_no = str(uuid.uuid4())
        pay_url = create_alipay_order(out_trade_no, total_amount, subject)
        return Response({'pay_url': pay_url}, status=status.HTTP_200_OK)

class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        password = data.get('password')

        try:
            user = User.objects.get(id=user_id)
            if password == user.password:
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'phone_number': user.phone_number,
            'is_admin': user.is_admin,
            'favorite_type_of_music': user.favorite_type_of_music
        }, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        password = data.get('password')
        phone_number = data.get('phone_number')
        code = data.get('code')

        stored_code = redis_client.get(phone_number)
        if stored_code and stored_code.decode('utf-8') == code:
            if User.objects.filter(id=user_id).exists():
                return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User(id=user_id, password=password, phone_number=phone_number)
            user.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '验证码无效或已过期'}, status=status.HTTP_400_BAD_REQUEST)