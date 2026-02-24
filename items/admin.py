from django.contrib import admin
from .models import Item
# Register your models here.

@admin.register(Item)
class Item_admin(admin.ModelAdmin):
    list_display = (
        "item_status",
        "item_num",
        "item_title",
        "item_desc",
        "item_cate",
        "select_tex",
        "item_price",
        "item_origin",
        "delivery_1",
        "delivery_2",
        "created_at",
        "updated_at"
    )