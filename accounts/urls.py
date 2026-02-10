from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("join/", views.join, name="join"),
    path("userJoin/", views.user_join, name="user_join"),
    path("mypage/", views.mypage, name="mypage"),
    path("excel_upload", views.order_excel, name="order_excel"),
    path("excel_sample_download", views.excel_sample_download, name="excel_sample_download")
]
