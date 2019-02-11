from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from main.decorators import charity_required, volunteer_required
from main.forms import CharityCreationForm, VolunteerCreationForm, ProjectCreationForm, PaymentCreationForm, \
    SkillCreationForm
from main.models import Project, VolunteerHasSkill, Charity, Volunteer, Opportunity


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
            return redirect('projects')
    else:
        form = ProjectCreationForm(charity=request.charity)
    return render(request, 'new_project.html', {'form': form})


def projects(request):
    objects = Project.objects.filter(end_time__isnull=True)
    return render(request, 'project_list.html', {'projects': objects})


def project(request, project_id):
    projects_list = Project.objects.filter(end_time__isnull=True)
    for p in projects_list:
        if p.id == project_id:
            matched_project = p
            project_type = 'غیر نقدی'
            if matched_project.project_type == 0:
                project_type = 'نقدی'
            opportunity = None
            for o in Opportunity.objects.all():
                if o.project.id == project_id:
                    opportunity = o

            return render(request, 'project.html', {'project': matched_project, 'project_type': project_type, 'opportunity': opportunity})
    return render(request, 'project_list.html', {'projects': projects_list})


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


def charity_list(request):
    objects = Charity.objects.all()
    project_lists = Project.objects.all()
    return render(request, 'charity_list.html', {'charities': objects, 'projects': project_lists})


def volunteer_list(request):
    objects = Volunteer.objects.all()
    return render(request, 'volunteer_list.html', {'volunteers': objects})


def charity(request, charity_id):
    project_lists = Project.objects.filter(end_time__isnull=True)
    charities_list = Charity.objects.all()
    for c in charities_list:
        if c.id == charity_id:
            matched_charity = c
            project_lists = Project.objects.filter(created_by=c)
            return render(request, 'charity.html', {'charity': matched_charity, 'projects': project_lists, 'opportunities': Opportunity.objects.all()})
    return render(request, 'charity_list.html', {'charities': charities_list, 'projects': project_lists})


def volunteer(request, volunteer_id):
    project_lists = Project.objects.filter(end_time__isnull=True)
    volunteers_list = Volunteer.objects.all()
    for c in volunteers_list:
        if c.id == volunteer_id:
            matched_volunteer = c
            return render(request, 'volunteer_view.html', {'volunteer': matched_volunteer, 'projects': project_lists, 'opportunities': Opportunity.objects.all()})
    return render(request, 'volunteer_list.html', {'volunteers': volunteers_list, 'projects': project_lists})


def my_projects(request):
    project_lists = Project.objects.filter(end_time__isnull=True)
    return render(request, 'my_projects.html', {'projects': project_lists, 'opportunities': Opportunity.objects.all()})


def my_settings(request):
    project_lists = Project.objects.filter(end_time__isnull=True)
    return render(request, 'settings.html', {'projects': project_lists, 'opportunities': Opportunity.objects.all()})


def mails(request):
    project_lists = Project.objects.filter(end_time__isnull=True)
    return render(request, 'mails.html', {'projects': project_lists, 'opportunities': Opportunity.objects.all()})
