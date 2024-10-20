from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Item, Category
from .forms import NewItemForm, EditItemForm

from django.http import JsonResponse

from cart.models import Pedido

import requests


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    releted_items = Item.objects.filter(category=item.category, sold=False).exclude(
        pk=item_id
    )[0:3]

    # data = {
    #   "product": {
    #         "id": item.id,
    #         "name": item.name,
    #         "description": item.description,
    #         "price": item.price,
    #         "sold": str(item.sold),
    #         "image": item.image.url,
    #         "category": item.category.id,
    #         "created_by": item.created_by.id
    #     },
    #   "quantity": 1
    # }

    # if request.POST.get("action") == "post":
        # # response = JsonResponse(item_dict_add)

        # return response 
        
        # redirect("core:index")

    if request.method == "POST":
        try:
            exclusive = get_object_or_404(Pedido, item=item, owner=request.user)
            endpoint_pedido = f"http://127.0.0.1:8000/pedido/{exclusive.id}/"
            delete_request_pedido = requests.delete(endpoint_pedido)

        except: # I gotta check what exception arise to make it more precise
            endpoint_pedido = "http://127.0.0.1:8000/pedido/"
            endpoint_cart = "http://127.0.0.1:8000/cart/"

            pedido = {
                "item": item.id,
                "owner": request.user.id,
                "quantity": 4,
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
            exclusive = get_object_or_404(Pedido, item=item, owner=request.user)
            show = False
        except:
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

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        "items": items,
        "query": query,
        "categories": categories,
        "category_id": int(category_id),
    }

    return render(request, "item/items.html", context)
