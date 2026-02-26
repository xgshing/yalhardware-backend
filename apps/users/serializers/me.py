# /me 接口
# apps/users/serializers/me.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMeSerializer(serializers.ModelSerializer):
    """
    当前登录用户信息序列化器
    只用于返回用户信息，不用于创建
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        )
