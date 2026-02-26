# Admin 用户管理 API
# apps/users/views/admin.py

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers.admin import AdminUserSerializer
from apps.users.permissions import IsAdminUser

User = get_user_model()


# 用户列表（GET)
class AdminUserListView(generics.ListAPIView):
    """
    管理员：用户列表
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]


# 用户详情（GET）
class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    """
    管理员：用户详情
    """

    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

    http_method_names = ["get", "patch"]


# 修改用户权限/状态（PATCH）
class AdminUserUpdateView(APIView):
    """
    管理员：修改用户状态/权限
    """

    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # 允许修改字段
        for field in ["is_staff", "is_active"]:
            if field in request.data:
                setattr(user, field, request.data[field])

        user.save()

        return Response(AdminUserSerializer(user).data, status=status.HTTP_200_OK)
