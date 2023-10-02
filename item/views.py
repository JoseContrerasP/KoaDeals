from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Item
from .forms import NewItemForm


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    releted_items = Item.objects.filter(category=item.category, sold=False).exclude(
        pk=item_id
    )[0:3]
    context = {"item": item, "releted_items": releted_items}
    return render(request, "item/detail.html", context)


@login_required
def new_item(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect("item:detail", item_id=item.id)

    else:
        form = NewItemForm()

    context = {"form": form, "title": "New Item"}
    return render(request, "item/new_item.html", context)
