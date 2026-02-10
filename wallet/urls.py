from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    path("deposit/", views.deposit, name="deposit"),
    path("use_list/", views.use_list, name="use_list"),
    path("refund/", views.refund, name="refund"),
    path("refund_list/", views.refund_list, name="refund_list"),
]
