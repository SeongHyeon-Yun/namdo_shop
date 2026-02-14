from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required


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
    count = range(100)
    return render(request, "manager/items.html", {"count": count})
