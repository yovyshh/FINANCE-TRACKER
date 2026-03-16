from django.urls import path
from .views import *
urlpatterns = [
    path('add_income/', add_income, name='add_income'),
    path('get_subcategories/<int:category_id>/', get_subcategories, name='get_subcategories'),
    path('income_list/', income_list, name='income_list'),
    path('income/delete/<int:income_id>/', delete_income, name='delete_income'),
    
    
    
    path('report', report_view, name='report_view'),
    path('filter-data/', filter_data, name='filter_data'),
    
    
    path('filter_superuser_categories', filter_superuser_categories, name='filter_superuser_categories'),
    path('common_report', common_report, name='common_report'),
    path('filter-categories/', filter_categories, name='filter_categories'),
    path('fetch_common_report_data', fetch_common_report_data, name='fetch_common_report_data'),
    # path('filter-expenses/', filter_expenses, name='filter_expenses'),
]
