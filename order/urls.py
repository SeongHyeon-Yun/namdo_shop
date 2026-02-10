from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('order_list', views.order_list, name="order_list"),
    path('delivery_ing', views.delivery_ing, name="delivery_ing"),
    path('delivery_done', views.delivery_done, name="delivery_done"),
    path('cancel', views.cancel, name="cancel"),
]
