from django.shortcuts import render, redirect

from item.models import Category, Item
from .forms import MySignupForm, LoginForm

from django.contrib.auth import login, logout, authenticate

from django.conf import settings

import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('C:\\Users\\18298\\Desktop\\Jose\\programming\\koadeals2\\.env')
load_dotenv(dotenv_path=dotenv_path)
# print(dotenv_path.exists())

def index(request):
    items = Item.objects.filter(sold=False).reverse()
    categories = Category.objects.all()
    context = {"items": items, "categories": categories}

    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")


def quick_login(request):
    user = authenticate(
        request,
        username=os.getenv("USUARIO"),
        password=os.getenv("PASSWORD"),
    )

    login(request, user)
    return redirect("core:index")


def signup(request):
    if request.method == "POST":

        if request.POST["guest"] == "true":
            return quick_login(request)

        else:
            form = MySignupForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("core:login")
            else:
                pass

    else:
        form = MySignupForm()

    context = {"form": MySignupForm}

    return render(request, "core/signup.html", context)


def signin(request):
    if request.method == "GET":
        context = {"form": LoginForm}

        return render(request, "core/login.html", context)

    else:

        if request.POST["guest"] == "true":
            return quick_login(request)

        else:
            user = authenticate(
                request,
                username=request.POST["username"],
                password=request.POST["password"],
            )

            if user:
                login(request, user)
                return redirect("core:index")

            else:
                return render(
                    request, "core/login.html", {"error": "Username or password incorrect"}
                )


def signout(request):
    logout(request)
    return redirect("core:index")


def payment_success(request):
    return render(request, "core/payment_success.html", {})


def payment_failed(request):
    return render(request, "core/payment_failed.html", {})
