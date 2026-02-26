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
