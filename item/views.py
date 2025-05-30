from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from .models import Item, Category
from .forms import NewItemForm, EditItemForm

from django.http import JsonResponse

from cart.models import Pedido

import requests

import cart as cart_


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    releted_items = Item.objects.filter(category=item.category, sold=False).exclude(
        pk=item_id
    )[0:3]

    if request.method == "POST":
        if settings.DEBUG:
            endpoint_default = settings.LOCAL_ENDPOINT
        else:
            endpoint_default = settings.deploy_endpoint

        try:
            exclusive = Pedido.objects.get(item=item, owner=request.user)

            # exclusive = get_object_or_404(Pedido, item=item, owner=request.user)
            # something = request.POST.get("value1", "value2")

            endpoint_pedido = f"{endpoint_default}pedido/{exclusive.id}/"
            # endpoint_pedido = f"https://koa-deals.onrender.com/pedido/{exclusive.id}/"
            delete_request_pedido = requests.delete(endpoint_pedido)

        except Pedido.DoesNotExist:
            endpoint_pedido = endpoint_default + "pedido/"
            endpoint_cart = endpoint_default + "cart/"

            pedido = {
                "item": item.id,
                "owner": request.user.id,
                "quantity": 1,
            }

            post_request_pedido = requests.post(endpoint_pedido, json=pedido)
            exclusive = Pedido.objects.get(item=item, owner=request.user)

            cart = {
                "pedido": exclusive.id 
            }

            post_request = requests.post(endpoint_cart, json=cart)
       
        return redirect("item:detail", item_id=item_id)


    else:
        try:
            if request.user.is_authenticated:
                exclusive = Pedido.objects.get(item=item, owner=request.user)
                show = False

            else:
                return redirect("core:login")

        except Pedido.DoesNotExist:
            show = True

        context = {"item": item, "releted_items": releted_items, "show": show}
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


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, created_by=request.user)
    item.delete()

    return redirect("dashboard:index")


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, created_by=request.user)

    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            item.save()

            return redirect("item:detail", item_id=item_id)

    else:
        form = EditItemForm(instance=item)

    context = {"item": item, "form": form}
    return render(request, "item/edit.html", context)


def items(request):
    items = Item.objects.filter(sold=False)
    query = request.GET.get("query", "")
    categories = Category.objects.all()
    category_id = request.GET.get("category", 0)
    category = None

    if category_id:
        items = items.filter(category_id=category_id)
        category = Category.objects.get(id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category and query:
        title = f"{query} in {category.name}"

    elif category:
        title = str(category.name)

    elif query:
        title = query

    else:
        title = "Items"

    context = {
        "items": items,
        "query": query,
        "categories": categories,
        "category_id": int(category_id),
        "category": category,
        "title": title,
    }

    return render(request, "item/items.html", context)
