from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import User, Project, Payment

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Payment)
