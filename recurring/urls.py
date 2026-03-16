from django.urls import path
from . import views

urlpatterns = [
    path('add_recurring/', views.add_recurring, name='add_recurring'),
    path('recurring_list/', views.view_recurring, name='recurring_list'),
]
