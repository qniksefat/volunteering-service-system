from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Admin(models.Model):
    name = models.CharField(max_length=255)


class Charity(User):
    approved_by = models.ForeignKey(Admin, on_delete=SET_NULL, null=True, blank=True)


BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3
LEVEL_CHOICES = (
    (BEGINNER, "beginner"),
    (INTERMEDIATE, "intermediate"),
    (EXPERT, "expert"),
)


class Volunteer(User):
    level = models.SmallIntegerField(choices=LEVEL_CHOICES, default=BEGINNER)
    skills = models.ManyToManyField('Skill', through='VolunteerHasSkill')


class Project(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(Charity, on_delete=SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(Admin, on_delete=SET_NULL, null=True, blank=True)
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
    level = models.SmallIntegerField(choices=LEVEL_CHOICES, default=BEGINNER)
    skill = models.ForeignKey(Skill, on_delete=CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=CASCADE)


class OpportunityNeedsSkill(models.Model):
    level = models.SmallIntegerField(choices=LEVEL_CHOICES, default=BEGINNER)
    skill = models.ForeignKey(Skill, on_delete=CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=CASCADE)


class Rating(models.Model):
    grade = models.SmallIntegerField()
    opportunity = models.ForeignKey(Opportunity, on_delete=CASCADE)
    charity = models.ForeignKey(Charity, on_delete=CASCADE)
    project = models.ForeignKey(Project, on_delete=CASCADE)
