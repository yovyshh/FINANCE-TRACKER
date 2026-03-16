# urls.py
from django.urls import path
from . import views
from .views import BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDetailView, BudgetDeleteView

urlpatterns = [
    path('budget_list', BudgetListView.as_view(), name='budget_list'),
    path('budget_form/', BudgetCreateView.as_view(), name='budget_form'),
    path('update/<int:pk>/', BudgetUpdateView.as_view(), name='budget_update'),
    path('detail/<int:pk>/', BudgetDetailView.as_view(), name='budget_detail'),
   
    path('budget/delete/<int:pk>/', BudgetDeleteView.as_view(), name='budget_delete'),
]



