from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE
from django.utils import timezone

BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3
LEVEL_CHOICES = (
    (BEGINNER, "beginner"),
    (INTERMEDIATE, "intermediate"),
    (EXPERT, "expert"),
)


class User(AbstractUser):
    ADMIN = 1
    CHARITY = 2
    VOLUNTEER = 3
    USER_TYPES = (
        (ADMIN, 'admin'),
        (CHARITY, 'charity'),
        (VOLUNTEER, 'volunteer'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=ADMIN)


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    approved_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='charities_approved')


class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=BEGINNER)
    skills = models.ManyToManyField('Skill', through='VolunteerHasSkill')


class Project(models.Model):
    FINANCIAL = 0
    NON_FINANCIAL = 1
    TYPES = (
        (FINANCIAL, 'Financial'),
        (NON_FINANCIAL, 'Non Financial'),
    )

    title = models.CharField(max_length=255)
    project_type = models.PositiveSmallIntegerField(choices=TYPES, default=FINANCIAL)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(Charity, on_delete=SET_NULL, null=True)
    approved_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='projects_approved')
    paid_by = models.ManyToManyField(Volunteer, through='Payment')


class Payment(models.Model):
    description = models.TextField(max_length=4095)
    amount = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=CASCADE)


class Opportunity(models.Model):
    description = models.TextField(max_length=4095)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=CASCADE)
    volunteers = models.ManyToManyField(Volunteer)
    needed_skills = models.ManyToManyField('Skill')


class Skill(models.Model):
    title = models.CharField(max_length=255)


class VolunteerHasSkill(models.Model):
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=BEGINNER)
    skill = models.ForeignKey(Skill, on_delete=CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=CASCADE)


class OpportunityNeedsSkill(models.Model):
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=BEGINNER)
    skill = models.ForeignKey(Skill, on_delete=CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=CASCADE)


class Rating(models.Model):
    grade = models.PositiveSmallIntegerField()
    opportunity = models.ForeignKey(Opportunity, on_delete=CASCADE)
    charity = models.ForeignKey(Charity, on_delete=CASCADE)
    project = models.ForeignKey(Project, on_delete=CASCADE)
