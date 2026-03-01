# 注册 / 登录
# apps/users/views/auth.py
"""
用户认证相关的API视图
包括用户注册和登录功能
"""

# apps/users/views.py
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers.auth import RegisterSerializer
from apps.users.serializers.me import UserMeSerializer

User = get_user_model()


class RegisterView(APIView):
    """
    用户视图

    处理新用户注册请求，创建用户账户
    使用RegisterSerializer进行数据验证和用户创建
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        处理POST请求-用户注册

        request:HTTP请求对象，包含注册数据
        """
        # 使用序列化器验证和转换数据
        serializer = RegisterSerializer(data=request.data)

        # 检查数据是否有效（符合序列化器定义的规则）
        if serializer.is_valid():
            # 数据有效，保存用户
            serializer.save()
            # 返回成功响应
            return Response(
                {"message": "Account created successfully"},
                status=201,
            )

        # 数据无效，返回验证错误信息
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    """
    用户登录视图
    使用邮箱和密码登录，返回 JWT Token 和完整用户信息
    支持前台和后台同一个接口：
    """

    permission_classes = [AllowAny]

    def post(self, request):

        # --- 获取请求数据 ---
        email = request.data.get("email")
        password = request.data.get("password")

        # 必填字段校验
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=400,
            )

        # 查找用户
        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=401)

        # 用户状态检查
        if not user.is_active:
            return Response({"error": "用户已被禁用"}, status=403)

        # -----------------------------
        # 角色限制（关键部分）
        # -----------------------------
        admin_mode = request.data.get("admin", False)

        if not admin_mode and user.is_staff:
            return Response({"error": "管理员账号请选择管理员身份登录"}, status=400)

        if admin_mode and not user.is_staff:
            return Response({"error": "该账号不是管理员"}, status=403)

        # --- 生成 JWT Token ---
        refresh = RefreshToken.for_user(user)

        # --- 序列化用户信息 ---
        user_data = UserMeSerializer(user).data

        # --- 返回响应 ---
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": user_data,
            }
        )
