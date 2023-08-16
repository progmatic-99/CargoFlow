from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from users.models import User


def loginPage(request):
    page = "login"
    error = ""

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            error = "User dont exist! Please Try Again"

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # email = user.email
            return redirect("index")
        else:
            error = "Credentials dont match. Please Try Again"

    loginPage_data = {"page": page, "error": error}
    return render(request, "shipping/login.html", loginPage_data)


def logoutUser(request):
    logout(request)
    return redirect("login")
