from django.db import models

class Item(models.Model):
    CATEGORY_CHOICES = [
        ("농산물", "농산물"),
        ("수산물", "수산물"),
        ("축산물", "축산물"),
        ("가공식품", "가공식품"),
        ("김치", "김치"),
        ("젓갈", "젓갈"),
        ("기타", "기타"),
    ]

    TAX_CHOICES = [
        ("과세", "과세"),
        ("면세", "면세"),
    ]

    STATUS_CHOICES = [
        ("stop", "중지"),
        ("sale", "판매중"),
    ]
    
    item_status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="sale")
    item_num = models.CharField(max_length=50, unique=True, blank=True)
    item_title = models.CharField(max_length=150)
    item_desc = models.TextField(null=True, blank=True)
    item_cate = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    select_tex = models.CharField(max_length=5, choices=TAX_CHOICES)
    item_price = models.PositiveIntegerField()
    item_origin = models.CharField(max_length=20)
    delivery_1 = models.PositiveIntegerField()
    delivery_2 = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.item_num:
            last_item = Item.objects.order_by("-id").first()
            next_number = 1 if not last_item else last_item.id + 1
            self.item_num = f"{next_number:06d}"  # 000001 형식

        super().save(*args, **kwargs)

    def __str__(self):
        return self.item_title
