# 启动钩子
# apps/users/apps.py
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.conf import settings
import os


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        """
        自动创建 superuser（仅生产环境 + Render）
        """
        # ❌ 本地开发不执行
        if settings.DEBUG:
            return

        # ❌ 未配置环境变量不执行
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            return

        User = get_user_model()

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            print("✅ Superuser created by UsersConfig")
