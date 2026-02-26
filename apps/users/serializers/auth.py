# 注册 / 登录
# apps/users/serializers/auth.py
"""
用户注册序列化器
处理用户注册时的数据验证和用户创建
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器

    继承自ModelSerializer, 提供模型字段的自动序列化/反序列化
    专门用于处理新用户注册请求
    """

    # 密码字段
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:

        model = User  # 关联的Django用户模型
        fields = ("email", "first_name", "last_name", "password")

    def validate_email(self, value):
        """
        邮箱验证方法

        检查邮箱是否已被注册，确保邮箱唯一性
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email alaready exists")
        return value

    def create(self, validated_data):
        """
        创建用户方法

        使用验证通过的数据创建新用户
        重写ModelSerializer 的默认create方法
        """
        user = User.objects.create_user(
            # 使用邮箱作为username字段的值（Django要求username必填)
            username=validated_data["email"],  # 将邮箱赋值给username字段
            # 实际邮箱字段
            email=validated_data["email"],
            # 名字字段，如果没有提供则使用空字条串
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            # 密码字段，create_user会自动进行哈希处理
            password=validated_data["password"],
        )
        return user
