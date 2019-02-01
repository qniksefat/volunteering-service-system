from django import forms
from django.contrib.auth.forms import UsernameField, UserCreationForm

from main.models import User, Charity, LEVEL_CHOICES, Volunteer, Project


class CharityCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.user_type = user.CHARITY
        user.save()
        Charity.objects.create(user=user)
        return user


class VolunteerCreationForm(UserCreationForm):
    level = forms.ChoiceField(choices=LEVEL_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'level',)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        assert commit
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.user_type = user.VOLUNTEER
        user.save()
        Volunteer.objects.create(user=user, level=self.cleaned_data['level'])
        return user


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        self.charity = kwargs.pop('charity')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        project = super().save(commit=False)
        project.created_by = self.charity
        if commit:
            project.save()
        return project
