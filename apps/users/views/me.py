# UserMeView
# apps/users/views/me.py
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.serializers.me import UserMeSerializer
from rest_framework.permissions import IsAuthenticated


class UserMeView(APIView):
    """
    获取当前登录用户信息
    GET/user/me/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserMeSerializer(user)
        return Response(serializer.data)
