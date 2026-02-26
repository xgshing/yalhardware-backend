# apps/reviews/admin.py
from django.contrib import admin
from .models.review import Review
from .models.review_reply import ReviewReply


class ReviewReplyInline(admin.StackedInline):
    model = ReviewReply
    extra = 0
    max_num = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_item",
        "user",
        "rating",
        "created_at",
    )

    list_filter = ("rating", "created_at")
    search_fields = (
        "order_item__order__order_no",
        "order_item__product_title",
        "user__username",
    )

    readonly_fields = (
        "order_item",
        "user",
        "rating",
        "content",
        "images",
        "created_at",
    )

    inlines = [ReviewReplyInline]
