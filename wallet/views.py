from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Deposit, Refund, Wallet


# Create your views here.
@login_required
def deposit(request):
    return render(request, "wallet/deposit.html")


@login_required
def use_list(request):
    deposit_list = Deposit.objects.filter(user=request.user)
    return render(request, "wallet/use_list.html", {"deposit_list": deposit_list})


@login_required
def refund(request):
    if request.method == "POST":
        bank = request.POST.get("bank")
        user_name = request.POST.get("user_name")
        bank_num = request.POST.get("bank_num")
        refund_value = request.POST.get("refund_value")

        result_refund_value = int(refund_value.replace(",", ""))

        try:
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(user=request.user)

                if result_refund_value <= 0:
                    raise ValueError("환급 금액이 올바르지 않습니다.")
                if result_refund_value > wallet.balance:
                    raise ValueError("보유머니가 부족합니다.")

                Refund.objects.create(
                    user=request.user,
                    bank=bank,
                    user_name=user_name,
                    bank_num=bank_num,
                    refund_value=result_refund_value,
                )

                wallet.balance -= result_refund_value
                wallet.save()

            messages.success(request, "환급 신청이 완료되었습니다.")
            return redirect("wallet:refund")

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("wallet:refund")

    return render(request, "wallet/refund.html")


@login_required
def refund_list(request):
    row_refund = Refund.objects.filter(user=request.user)

    return render(request, "wallet/refund_list.html", {"row_refund": row_refund})
