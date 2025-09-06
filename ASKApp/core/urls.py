from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register/logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('ask/', views.ask, name='ask'),
    path('about/', views.about, name='about'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('identify/', views.identify, name='identify'),
    path('answer/<int:id>/', views.answer, name='answer'),
    #path('questions/',views.questions,name='questionsList'),
    path('archive/',views.archive,name='archive'),
    path('question/<int:id>/',views.question_answers,name='question'),
    path('vote/<int:id>/<str:flag>/',views.toggle_vote,name='vote'),
    path('notifications/',views.notifications,name='notifications'),
    path('mark_notifications_as_read/<int:id>/',views.mark_notifications_as_read,name='mark_notifications_as_read'),
    
]