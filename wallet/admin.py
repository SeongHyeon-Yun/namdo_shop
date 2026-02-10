from django.contrib import admin
from .models import Deposit, Wallet, Refund


@admin.register(Deposit)
class Deposit_admin(admin.ModelAdmin):
    list_display = (
        "user",
        "company_name",
        "deposit_value",
        "deposit_name",
        "deposit_status",
        "is_applied",
        "created_at",
        "confirmed_at",
        "admin_memo",
    )


@admin.register(Wallet)
class user_wallet(admin.ModelAdmin):
    list_display = ("user", "balance")


@admin.register(Refund)
class Refund_list(admin.ModelAdmin):
    list_display = (
        "user",
        "bank",
        "user_name",
        "bank_num",
        "refund_value",
        "created_at",
        "confirmed_at",
        "is_applied",
        "refund_status",
        "admin_memo",
    )
