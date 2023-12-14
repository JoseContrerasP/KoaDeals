from django.shortcuts import render, redirect

from item.models import Category, Item
from .forms import SignupForm

from django.contrib.auth import logout


def index(request):
    items = Item.objects.filter(sold=False)
    categories = Category.objects.all()
    context = {"items": items, "categories": categories}

    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("core:login")

    else:
        form = SignupForm()

    context = {"form": SignupForm}

    return render(request, "core/signup.html", context)


def signout(request):
    logout(request)
    return redirect("core:index")
