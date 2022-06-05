from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import  HttpResponseBadRequest
from django.contrib.auth.models import User

def firstpage(request):
    return render(request, 'accounts/first_page.html')

def form_new_user(request):
    form = NewUserForm()
    return HttpResponseBadRequest(
        render(
            request=request,
            template_name="accounts/register.html",
            context={"register_form": form},
        )
    )


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            username = User.objects.filter(username=order.username)
            if username:

                form_new_user(request)
            else:
                mail = order.email
                email_from_bd = User.objects.filter(email=mail)
                if email_from_bd:
                    assert HttpResponseBadRequest(form_new_user(request))
                else:
                    user = form.save()
                    login(request, user)
                    messages.success(request, "Registration successful.")
                    return redirect("profile_user")
    return HttpResponseBadRequest(form_new_user(request))


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("profile_user")
    form = AuthenticationForm()
    return HttpResponseBadRequest(
        render(
            request=request,
            template_name="accounts/login.html",
            context={"login_form": form},
        )
    )


def logout_request(request):
    logout(request)
    return redirect("firstpage")

