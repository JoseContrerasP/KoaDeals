from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import Http404
import requests

from item.models import Category, Item
from .forms import MySignupForm, LoginForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.conf import settings

import os
from dotenv import load_dotenv
from pathlib import Path

from cart.models import Pedido, Cart

if settings.DEBUG:
    dotenv_path = Path('C:\\Users\\18298\\Desktop\\Jose\\programming\\koadeals2\\.env')
else:
    dotenv_path = Path('home/koadeals/koadeals/')
load_dotenv(dotenv_path=dotenv_path)

def index(request):
    items = Item.objects.filter(sold=False).reverse()
    categories = Category.objects.all()
    context = {"items": items, "categories": categories}

    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")


def quick_login(request, guest=True):
    if guest:
        user = authenticate(
            request,
            username=os.getenv("USUARIO"),
            password=os.getenv("PASSWORD"),
        )

    else:
        # password = request.POST.get('password') or request.POST.get('password1')

        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST.get('password1'),
        )

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("core:index")


def signup(request):
    if request.method == "POST":

        if request.POST["guest"] == "true":
            return quick_login(request)

        else:
            form = MySignupForm(request.POST)

            if form.is_valid():
                form.save()
                return quick_login(request, False)

            else:
                context = {"form": form}
                return render(request, "core/signup.html", context)

    else:
        form = MySignupForm()

        context = {"form": form}

        return render(request, "core/signup.html", context)


def signin(request):
    if request.method == "GET":
        context = {"form": LoginForm}

        return render(request, "core/login.html", context)

    else:
        if request.POST["guest"] == "true":
            return quick_login(request)

        else:
            form = LoginForm(request.POST)
            error = ""

            try:
                user = get_object_or_404(User, username=request.POST["username"])

                user = authenticate(
                    request,
                    username=user.username,
                    password=request.POST["password"],
                )

                if user:
                    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                    return redirect("core:index")

                else:
                    error = "Sorry, your password was incorrect. Please double-check your password."

            except Http404:
                error = "There is no user registered with that username."

            context = {"form": form, "error": error}
            return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("core:index")


@login_required
def payment_success(request):
    pedidos = Pedido.objects.filter(owner=request.user)

    if settings.DEBUG:
        default_endpoint = settings.LOCAL_ENDPOINT
    else:
        default_endpoint = settings.DEPLOY_ENDPOINT

    total = 0
    quantities = 0
    for pedido in pedidos:        
        total += pedido.get_total_pedido()
        quantities += pedido.quantity

        endpoint = default_endpoint + "pedido/"
        
        endpoint += str(pedido.id) + "/"
        request_delete = requests.delete(endpoint)

    context = {"pedidos": pedidos, "total": total, "quantities": quantities}

    return render(request, "core/payment_success.html", context)


@login_required
def payment_failed(request):
    return render(request, "core/payment_failed.html", {})
