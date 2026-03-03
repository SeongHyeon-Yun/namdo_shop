from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import FileResponse
from django.conf import settings
from .forms import join_form, ExcelUploadForm
from .models import User
from wallet.models import Wallet
import os


# Create your views here.
def login(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("main:index")
        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "아이디 또는 비밀번호가 올바르지 않습니다."},
            )

    return render(request, "accounts/login.html")


def logout(request):
    auth_logout(request)
    return redirect("main:index")


def join(request):
    return render(request, "accounts/join.html")


def user_join(request):
    if request.method == "POST":
        form = join_form(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data.copy()

            password = data.pop("password_1")
            data.pop("password_2")

            user = User.objects.create_user(password=password, **data)
            Wallet.objects.create(user=user)

            messages.success(request, "회원가입이 완료 되었습니다.")
            return redirect("accounts:login")

    else:
        form = join_form()

    return render(request, "accounts/user-info.html", {"form": form})


@login_required
def mypage(request):
    return render(request, "accounts/mypage.html", {"rows": range(150)})


# 엑셀 업로드
@login_required
def order_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel = form.save(commit=False)
            excel.user = request.user
            excel.company_name = request.user.company_name
            excel.save()

            messages.success(request, "엑셀이 정상적으로 업로드 되었습니다.")
            return redirect("accounts:order_excel")
    else:
        form = ExcelUploadForm()

    return render(
        request,
        "accounts/excel_upload.html",
        {
            "form": form,
        },
    )


# 엑셀 샘플 다운로드
def excel_sample_download(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "sample/sample.xlsx")
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="주문_엑셀_양식.xlsx"
    )
