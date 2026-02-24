from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .utils import get_manager_item
from items.forms import Item_form
from items.models import Item
from django.http import JsonResponse


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
        {
            "current_status": status,
            "search": search,
            "page": page_obj,
        }
    )

    return render(request, "manager/items.html", context)


# 상품 등록 기능
def create_item(request):
    if request.method == "POST":
        form = Item_form(request.POST, request.FILES)

        if form.is_valid():
            print(form.errors)

            form.save()
            messages.success(request, "상품 등록이 완료 되었습니다.")
            return redirect("manager:items")

        else:
            print(form.item_status)
            messages.error(request, "상품 번호가 중복됩니다.")
            return redirect("manager:items")


# 등록된 상품 삭제 기능
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
def item_detail(request, pk):
    item = Item.objects.get(pk=pk)

    print(item.delivery_1)

    return JsonResponse(
        {
            "title": item.item_title,
            "price": item.item_price,
            "origin": item.item_origin,
            "delivery_1": item.delivery_1,
            "delivery_2": item.delivery_2,
            "text": item.select_tex,
            "status": item.get_item_status_display(),
            "description": item.description,
        }
    )
