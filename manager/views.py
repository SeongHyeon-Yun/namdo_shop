from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .utils import get_manager_item
from items.forms import Item_form
from items.models import Item, Thumnbnail
from accounts.models import User
from wallet.models import Deposit, Wallet, Refund
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.utils import timezone
from django.urls import reverse
from django.db import transaction


@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def index(request):
    count = range(2)
    return render(request, "manager/index.html", {"count": count})


@never_cache
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("manager:index")

    if request.method == "POST":
        id = request.POST.get("manager_id")
        pw = request.POST.get("manager_pw")

        user = authenticate(request, username=id, password=pw)

        if user and user.is_staff:
            login(request, user)
            return redirect("manager:index")
        else:
            msg = messages.error(request, "아이디 또는 비밀번호를 확인해주세요")
            return redirect("manager:login_view")

    return render(request, "manager/login.html")


@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def logout_view(request):
    logout(request)

    return redirect("manager:login_view")


@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def items(request):
    status = request.GET.get("status", "ALL")
    search = request.GET.get("search", "")
    search_type = request.GET.get("search_type", "title")
    form = Item_form()

    queryset = Item.objects.all()

    # 상태 필터
    if status != "ALL":
        queryset = queryset.filter(item_status=status)

    # 검색
    if search:
        if search_type == "title":
            queryset = queryset.filter(item_title__icontains=search)
        elif search_type == "number":
            queryset = queryset.filter(item_num__icontains=search)

    queryset = queryset.order_by("-id")

    paginator = Paginator(queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = get_manager_item()
    context.update(
        {"current_status": status, "search": search, "page": page_obj, "form": form}
    )

    return render(request, "manager/items.html", context)


@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def create_item(request):
    if request.method == "POST":
        form = Item_form(request.POST, request.FILES)

        if form.is_valid():

            # 1️⃣ 상품 먼저 저장
            item = form.save()

            # 2️⃣ 썸네일 여러 개 가져오기
            images = request.FILES.getlist("images")

            if not images:
                messages.error(request, "썸네일 이미지를 1개 이상 등록해주세요.")
                item.delete()
                return redirect("manager:items")

            # 3️⃣ 썸네일 저장
            for idx, img in enumerate(images):
                Thumnbnail.objects.create(
                    item=item, image=img, is_main=True if idx == 0 else False
                )

            messages.success(request, "상품 등록이 완료되었습니다.")
            return redirect("manager:items")

        else:
            messages.error(request, "입력값을 확인해주세요.")
            return redirect("manager:items")


# 등록된 상품 삭제 기능
@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def delete_item(request):
    if request.method == "POST":
        ids = request.POST.getlist("item_ids")
        print(ids)

        if not ids:
            messages.error(request, "삭제할 상품을 선택하세요")
            return redirect("manager:items")

        else:
            Item.objects.filter(id__in=ids).delete()
            messages.success(request, "삭제가 완료 되었습니다.")
            return redirect("manager:items")


# 상품 디테일 창
@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def item_detail(request, pk):
    item = Item.objects.get(pk=pk)
    imgs = item.images.all()

    img_list = [i.image.url for i in imgs]

    return JsonResponse(
        {
            "title": item.item_title,
            "price": item.item_price,
            "origin": item.item_origin,
            "tex": item.select_tex,
            "status": item.get_item_status_display(),
            "desc": item.description,
            "img_list": img_list,
            "delivery_1": item.delivery_1,
            "delivery_2": item.delivery_2,
        }
    )


# 상품 설명 이미지 업로드
def upload(request):
    if request.method == "POST" and request.FILES.get("upload"):
        file = request.FILES["upload"]
        path = default_storage.save(f"editor/{file.name}", file)
        file_url = default_storage.url(path)

        return JsonResponse({"url": file_url})

    return JsonResponse({"error": "업로드 실패"}, status=400)


# 유저 관리
def user_list(request):

    search_type = request.GET.get("search_type")
    search = request.GET.get("search")

    queryset = User.objects.filter(is_staff=False).order_by("-id")

    # 🔍 검색 필터
    if search and search_type:
        if search_type == "company_name":
            queryset = queryset.filter(company_name__icontains=search)

        elif search_type == "manager_name":
            queryset = queryset.filter(manager_name__icontains=search)

        elif search_type == "company_number":
            queryset = queryset.filter(company_number__icontains=search)

    # 📄 페이지네이션
    paginator = Paginator(queryset, 20)  # 한 페이지 10개
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "manager/user.html",
        {
            "page_obj": page_obj,
            "search": search,
            "search_type": search_type,
        },
    )


# 예치금 관리자 페이지
@never_cache
@staff_member_required(login_url="/manager/login")
@login_required
def deposit_page(request):
    now = timezone.now()
    status = request.GET.get("status", "deposit_pending")

    context = {"status": status}

    # ----------------------------
    # GET 데이터 처리 (목록 출력)
    # ----------------------------
    type_prefix, current_status = status.split("_")

    if type_prefix == "deposit":
        wallet_list = Deposit.objects.select_related("user").filter(
            deposit_status=current_status
        )
    else:
        wallet_list = Refund.objects.select_related("user").filter(
            refund_status=current_status
        )

    context.update({"wallet_list": wallet_list})

    # ----------------------------
    # POST 처리
    # ----------------------------
    if request.method == "POST":
        action = request.POST.get("action")
        object_id = request.POST.get("deposit_id")

        if not action or not object_id:
            messages.error(request, "잘못된 요청입니다.")
            return redirect(reverse("manager:deposit_page") + f"?status={status}")

        # ============================
        # 예치금 처리
        # ============================
        if action.startswith("deposit"):

            with transaction.atomic():
                deposit = Deposit.objects.select_for_update().get(id=object_id)

                if deposit.is_applied:
                    messages.warning(request, "이미 처리된 건입니다.")
                    return redirect(
                        reverse("manager:deposit_page") + f"?status={status}"
                    )

                wallet = deposit.user.wallet

                if action == "deposit_approve":
                    wallet.balance += deposit.deposit_value
                    deposit.deposit_status = "confirmed"
                    messages.success(request, "입금 승인 완료되었습니다.")

                elif action == "deposit_reject":
                    deposit.deposit_status = "rejected"
                    messages.error(request, "입금 신청이 거절되었습니다.")

                deposit.is_applied = True
                deposit.confirmed_at = now

                wallet.save()
                deposit.save()

        # ============================
        # 환불 처리
        # ============================
        elif action.startswith("refund"):

            with transaction.atomic():
                refund = Refund.objects.select_for_update().get(id=object_id)

                if refund.is_applied:
                    messages.warning(request, "이미 처리된 건입니다.")
                    return redirect(
                        reverse("manager:deposit_page") + f"?status={status}"
                    )

                wallet = refund.user.wallet

                if action == "refund_approve":
                    refund.refund_status = "confirmed"
                    messages.success(request, "환불 신청이 완료되었습니다.")

                elif action == "refund_reject":
                    wallet.balance += refund.refund_value
                    refund.refund_status = "rejected"
                    messages.error(request, "환불 신청이 거절되었습니다.")

                refund.is_applied = True
                refund.confirmed_at = now

                wallet.save()
                refund.save()

        return redirect(reverse("manager:deposit_page") + f"?status={status}")

    return render(request, "manager/deposit.html", context)
