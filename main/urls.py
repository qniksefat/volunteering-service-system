from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_projects/', views.my_projects, name='my_projects'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('charity/signup/', views.charity_signup, name='charity_signup'),
    path('volunteer/signup/', views.volunteer_signup, name='volunteer_signup'),
    path('volunteer/', views.volunteer_page, name='volunteer_page'),
    path('volunteer/<int:volunteer_id>/', views.volunteer, name='volunteer'),
    path('projects/new/', views.new_project, name='create_project'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project, name='project'),
    path('projects/<int:project_id>/pay', views.create_payment, name='create_payment'),
    path('charity/list/', views.charity_list, name='charities'),
    path('charity/<int:charity_id>/', views.charity, name='charity'),
    path('volunteer/list/', views.volunteer_list, name='volunteers'),
]
