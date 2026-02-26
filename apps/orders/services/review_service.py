# 评论追评 & 商家回复 Service
# apps/reviews/services/review_service.py
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.reviews.models import Review, ReviewReply


class ReviewService:
    """
    评论域业务逻辑（上线冻结）
    """

    @staticmethod
    @transaction.atomic
    def append_review(*, review: Review, content: str):
        """
        用户追评（只允许一次）
        """
        if review.append_content:
            raise ValidationError("该评论已追评")

        review.append_content = content
        review.append_at = timezone.now()
        review.save(update_fields=["append_content", "append_at"])

        return review

    @staticmethod
    @transaction.atomic
    def reply_review(*, review: Review, content: str, is_merchant=True):
        """
        商家 / 客服回复（OneToOne）
        """
        if hasattr(review, "reply"):
            raise ValidationError("该评论已回复")

        return ReviewReply.objects.create(
            review=review,
            content=content,
            is_merchant=is_merchant,
        )
