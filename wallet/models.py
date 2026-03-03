from django.db import models
from django.conf import settings


# 예치금 충전 테이블
class Deposit(models.Model):

    STATUS_CHOICES = (
        ("pending", "대기"),
        ("confirmed", "완료"),
        ("refund", "환불"),
        ("rejected", "반려"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, help_text="회사 명")

    deposit_value = models.PositiveIntegerField(help_text="입금 신청 금액")
    deposit_name = models.CharField(max_length=50, help_text="입금 신청자 명")

    deposit_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", help_text="입금 상태"
    )

    is_applied = models.BooleanField(default=False, help_text="입금 중복 방지 장치")

    created_at = models.DateTimeField(auto_now_add=True, help_text="입금 신청 시간")
    confirmed_at = models.DateTimeField(
        null=True, blank=True, help_text="입금 승인 시간"
    )

    admin_memo = models.TextField(blank=True, help_text="관리자 메모용")

    def __str__(self):
        return f"{self.user} - {self.deposit_value}원 ({self.deposit_status})"


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user} | {self.balance}원"


class Refund(models.Model):
    STATUS_CHOICES = (
        ("pending", "대기"),
        ("confirmed", "완료"),
        ("rejected", "반려"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank = models.CharField(max_length=10, help_text="은행 명")
    user_name = models.CharField(max_length=5, help_text="예금주")
    bank_num = models.CharField(max_length=50, help_text="계좌번호")
    refund_value = models.PositiveIntegerField(help_text="환급 금액")
    created_at = models.DateTimeField(auto_now_add=True, help_text="신청 시간")
    confirmed_at = models.DateTimeField(
        null=True, blank=True, help_text="환급 승인 시간"
    )
    is_applied = models.BooleanField(default=False, help_text="환급 중복 방지 장치")
    refund_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", help_text="환급 상태"
    )

    admin_memo = models.TextField(blank=True, help_text="관리자 메모용")

    def __str__(self):
        return f"{self.user} 환급"
