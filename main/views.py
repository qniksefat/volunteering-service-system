from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from main.decorators import charity_required, volunteer_required
from main.forms import CharityCreationForm, VolunteerCreationForm, ProjectCreationForm, PaymentCreationForm, \
    SkillCreationForm
from main.models import Project, VolunteerHasSkill


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
    return render(request, 'charity_signup.html', {'form': form})


def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = VolunteerCreationForm()
    return render(request, 'volunteer_signup.html', {'form': form})


@charity_required
def new_project(request):
    if request.method == 'POST':
        form = ProjectCreationForm(data=request.POST, charity=request.charity)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectCreationForm(charity=request.charity)
    return render(request, 'new_project.html', {'form': form})


def projects(request):
    objects = Project.objects.filter(end_time__isnull=True)
    return render(request, 'project_list.html', {'projects': objects})


@volunteer_required
def create_payment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not project.project_type == Project.FINANCIAL:
        raise Http404('non financial project has no payment')

    if request.method == 'POST':
        form = PaymentCreationForm(data=request.POST, volunteer=request.volunteer, project=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PaymentCreationForm(volunteer=request.volunteer, project=project)
    return render(request, 'payment.html', {'form': form})


@volunteer_required
def volunteer_page(request):
    if request.method == 'POST':
        form = SkillCreationForm(data=request.POST)
        if form.is_valid():
            skill = form.save()
            VolunteerHasSkill.objects.create(skill=skill,
                                             level=form.cleaned_data['level'],
                                             volunteer=request.volunteer)
            return redirect('volunteer_page')
    else:
        form = SkillCreationForm()

    objects = VolunteerHasSkill.objects.filter(volunteer=request.volunteer)
    return render(request, 'volunteer.html', {'form': form, 'skills': objects})
