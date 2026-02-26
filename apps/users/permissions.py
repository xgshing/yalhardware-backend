# 自定义权限
# apps/users/permissions.py
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    仅允许is_staff=True的用户访问
    普通用户 → 403
    管理员 → 放行
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
