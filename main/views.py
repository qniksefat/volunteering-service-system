from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from main.forms import CharityCreationForm, VolunteerCreationForm


class MyLoginView(LoginView):
    template_name = 'login.html'


class MyLogoutView(LogoutView):
    template_name = 'logout.html'


@login_required
def home(request):
    return render(request, 'home.html')


def charity_signup(request):
    if request.method == 'POST':
        form = CharityCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CharityCreationForm()
    return render(request, 'signup.html', {'form': form})


def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = VolunteerCreationForm()
    return render(request, 'signup.html', {'form': form})
