# 后台用户管理
# apps/users/serializers/admin.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """
    后台用户管理序列化器
    """

    class Meta:

        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "is_active",  # 是否激活
            "date_joined",  # 注册时间
            "last_login",  # 最后一次登录时间
        )
