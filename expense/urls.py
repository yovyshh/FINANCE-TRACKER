from django.urls import path
from . import views

urlpatterns = [
    path('list_expense/', views.  list_expenses, name='list_expense'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('budget_history/', views.budget_history, name='budget_history'),
    path('budget_history/<int:budget_id>/', views.budget_history, name='budget_history'),

]



