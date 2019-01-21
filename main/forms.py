from django import forms
from django.contrib.auth.forms import UsernameField, UserCreationForm

from main.models import User, Charity, LEVEL_CHOICES, Volunteer


class CharityCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
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
        fields = ('username', 'level',)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.user_type = user.VOLUNTEER
        user.save()
        Volunteer.objects.create(user=user, level=self.cleaned_data['level'])
        return user
