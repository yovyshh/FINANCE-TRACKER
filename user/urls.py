from django.contrib import admin
from . import views
from django.urls import path , include

urlpatterns = [
  path('',views.home),
  path('signin',views.signin),
  path('register',views.register),
  path('viewusers',views.viewuser),
  path('logout',views.dologout),
  path('service', views.service),
  path('about', views.about),
  path('index',views.home),
  path('contact',views.contact),

  

    
]