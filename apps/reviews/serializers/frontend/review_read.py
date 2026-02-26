# 评论读取 Serializer（含追评 & 商家回复）
# apps/reviews/serializers/frontend/review_read.py
from rest_framework import serializers
from apps.reviews.models import Review, ReviewReply


class ReviewReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReply
        fields = [
            "merchant_reply",
            "merchant_replied_at",
        ]


class ReviewReadSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    can_append = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "content",
            "images",
            "created_at",
            "append_content",
            "append_at",
            "reply",
            "can_append",
        ]

    def get_reply(self, obj):
        try:
            return ReviewReplySerializer(obj.reply).data
        except ReviewReply.DoesNotExist:
            return None

    def get_can_append(self, obj):
        # 是否可以追评
        return obj.append_content == ""
