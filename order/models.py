from django.db import models
from django.conf import settings


class Order(models.Model):

    STATUS_CHOICES = [
        ("READY", "상품준비중"),
        ("SHIPPING", "배송중"),
        ("DONE", "배송완료"),
        ("CANCEL", "취소"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_num = models.CharField(max_length=20, unique=True, help_text="주문번호")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="READY"
    )

    product_name = models.CharField(max_length=100, help_text="상품명")
    option_name = models.CharField(max_length=50, help_text="상품 옵션")
    quantity = models.PositiveIntegerField(help_text="구매 수량")

    receiver_name = models.CharField(max_length=20, help_text="수취인 이름")
    receiver_phone = models.CharField(max_length=20, help_text="수취인 번호")
    post_code = models.CharField(max_length=10, help_text="우편 번호")
    address = models.CharField(max_length=255, help_text="주소")
    delivery_msg = models.CharField(max_length=255, blank=True, help_text="배송 메세지")

    order_name = models.CharField(max_length=20, help_text="주문자 이름")
    order_phone = models.CharField(max_length=20, help_text="주문자 번호")

    created_at = models.DateTimeField(auto_now_add=True, help_text="주문 날짜")

    def __str__(self):
        return f"{self.order_num}"