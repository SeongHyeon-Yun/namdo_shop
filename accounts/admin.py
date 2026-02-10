from django.contrib import admin
from .models import User, ExcelUpload

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 목록 화면에 보일 컬럼
    list_display = (
        "user_id",
        "boss_name",
        "email",
        "phone",
        "company_name",
        "company_number",
        "manager_name",
        "business_file",
        "post_code",
        "address",
        "detail_address",
        "extraAddress",
        "email_check",
        "message_check",
        "is_active",
        "is_staff",
    )

    # 검색 가능 필드
    search_fields = ("user_id",)

    # 필터 (우측)
    list_filter = ("is_staff", "is_active")

    # 수정 화면에서 읽기 전용
    readonly_fields = ("last_login",)

    # 기본 정렬
    ordering = ("-id",)


@admin.register(ExcelUpload)
class Excel_admin(admin.ModelAdmin):
    list_display = ("excel_file", "company_name", "user", "created_at")
    ordering = ("-id",)
