# 追评 Serializer
from rest_framework import serializers
from django.utils import timezone
from apps.reviews.models import Review


class ReviewAppendSerializer(serializers.Serializer):
    review_id = serializers.IntegerField()
    content = serializers.CharField()

    def validate_review_id(self, value):
        user = self.context["request"].user

        try:
            review = Review.objects.get(id=value)
        except Review.DoesNotExist:
            raise serializers.ValidationError("评价不存在")

        if review.user != user:
            raise serializers.ValidationError("无权限追加评价")

        if review.append_content:
            raise serializers.ValidationError("已追加过评价")

        return value

    def save(self):
        review = Review.objects.get(id=self.validated_data["review_id"])
        review.append_content = self.validated_data["content"]
        review.append_at = timezone.now()
        review.save()
        return review
