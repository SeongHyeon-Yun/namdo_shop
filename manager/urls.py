from django.urls import path
from . import views

app_name = "manager"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("items/", views.items, name="items"),
    path("create_item/", views.create_item, name="create_item"),
    path("delete_item/", views.delete_item, name="delete_item"),
    path("item_detail/<int:pk>/", views.item_detail, name="item_detail"),
    path("user/", views.user_list, name="user_list"),
]
