from django.shortcuts import render, get_object_or_404
from .models import Item


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    releted_items = Item.objects.filter(category=item.category, sold=False).exclude(
        pk=item_id
    )[0:3]
    context = {"item": item, "releted_items": releted_items}
    return render(request, "item/detail.html", context)
