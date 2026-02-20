from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from .utils import get_manager_item
from items.forms import Item_form


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

    context = get_manager_item()
    context["count"] = range(100)
    context["current_status"] = status

    return render(request, "manager/items.html", context)


def create_item(request):
    if request.method == "POST":
        form = Item_form(request.POST, request.FILES)
        print("is_valid:", form.is_valid())
        print("errors:", form.errors)

        if form.is_valid():
            form.save()
            messages.success(request,"상품 등록이 완료 되었습니다.")
            return redirect("manager:items")

        else:
            messages.error(request, "상품 번호가 중복됩니다.")
            return redirect("manager:items")
    # return render(request, "manager/create_item.html", {"form": form})