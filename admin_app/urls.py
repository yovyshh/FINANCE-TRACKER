from django.contrib import admin
from . import views
from django.urls import path , include

urlpatterns = [
  path('add-category', views.category, name='add_category'),
  path('viewusers', views.viewuser, name='view_users'),
  path('viewcategories', views.viewcategory),
  
    
]