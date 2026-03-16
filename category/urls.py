from django.urls import path
from . import views

urlpatterns = [
    path('view_categories/', views.view_categories, name='view_categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category/<int:category_id>/add_subcategory/', views. view_subcategories, name='add_subcategory'),
    path('edit_subcategory/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete_subcategory/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory')




]
