from django.contrib import admin
from .models import Order


@admin.register(Order)
class Order_admin(admin.ModelAdmin):
    list_display = (
        "user",
        "order_num",
        "status",
        "product_name",
        "option_name",
        "quantity",
        "receiver_name",
        "receiver_phone",
        "post_code",
        "address",
        "delivery_msg",
        "order_name",
        "order_phone",
        "created_at",
    )
