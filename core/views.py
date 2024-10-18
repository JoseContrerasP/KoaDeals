from django.shortcuts import render, redirect

from item.models import Category, Item
from .forms import MySignupForm

from django.contrib.auth import logout


def index(request):
    items = Item.objects.filter(sold=False).reverse()
    categories = Category.objects.all()
    context = {"items": items, "categories": categories}

    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")


def signup(request):
    if request.method == "POST":
        form = MySignupForm(request.POST)

        if form.is_valid():
            form.save()
            print("Before you go")
            return redirect("core:login")
        else:
            pass

    else:
        form = MySignupForm()

    context = {"form": MySignupForm}

    return render(request, "core/signup.html", context)


def signout(request):
    logout(request)
    return redirect("core:index")
