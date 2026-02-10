from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError("user_id는 필수입니다.")

        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None):
        user = self.create_user(user_id, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, unique=True)
    boss_name = models.CharField(max_length=30, help_text="대표자 이름")
    email = models.CharField(max_length=50, help_text="이메일")
    phone = models.CharField(max_length=11, help_text="전화 번호")
    company_name = models.CharField(max_length=30, help_text="사업자 명")
    company_number = models.CharField(max_length=15, help_text="사업자 번호")
    manager_name = models.CharField(max_length=5, help_text="담당자 이름")
    business_file = models.FileField(
        upload_to="business_files/", verbose_name="사업자 등록증 파일"
    )
    post_code = models.CharField(max_length=20, help_text="우편 번호")
    address = models.CharField(max_length=100, help_text="주소")
    detail_address = models.CharField(max_length=100, help_text="상세주소")
    extraAddress = models.CharField(max_length=100, help_text="주소 참고 사항")
    email_check = models.BooleanField(default=False)
    message_check = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_id


class ExcelUpload(models.Model):
    excel_file = models.FileField(
        upload_to="excel_files/",
        verbose_name="엑셀 주문 파일",
    )
    company_name = models.CharField(
        max_length=30,
        help_text="주문 사업자 이름",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="excel_uploads",
        verbose_name="업로드 사용자",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.user}"
