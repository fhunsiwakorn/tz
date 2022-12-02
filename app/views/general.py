from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth

from ..common import defaultTitle


def login(request):
    title = defaultTitle
    context = {'title': title}
    if request.user.id is not None:
        return redirect("/")
    return render(request, 'login.html', context)


def login_check(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect("/")
    else:
        messages.error(
            request, "Invalid Credentials Error With Correct Username/Password")
        return redirect("/login")


def logout(request):
    auth.logout(request)
    return redirect("/login")


def handler404(request, exception):
    return render(request, '404.html')
