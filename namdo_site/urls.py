from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("accounts/", include("accounts.urls")),
    path("order/", include("order.urls")),
    path("wallet/", include("wallet.urls")),
    path("manager/", include("manager.urls")),
]
