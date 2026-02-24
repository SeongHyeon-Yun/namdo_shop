from django.shortcuts import render, redirect
from items.models import Item


# Create your views here.
def index(reqeust):
    items = Item.objects.all().order_by("-id")

    context = {"items": items}
    return render(reqeust, "main/index.html", context)
