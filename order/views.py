from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# 상품 준비중
@login_required
def order_list(request):
    return render(request, "order/order_list.html")


# 배송중
@login_required
def delivery_ing(request):
    return render(request, "order/delivery_ing.html")


# 배송완료
@login_required
def delivery_done(request):
    return render(request, "order/delivery_done.html")


# 취소
@login_required
def cancel(request):
    return render(request, "order/cancel.html")
