from django.shortcuts import render

from item.models import Category, Item


def index(request):
    items = Item.objects.filter(sold=False)
    categories = Category.objects.all()
    context = {"items": items, "categories": categories}

    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")


# Create your views here.
