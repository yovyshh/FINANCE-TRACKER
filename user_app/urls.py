from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MyModelListView, MyModelUpdateView, MyModelCreateView
# from .views import ShopRegistrationView, ApproveShopView
from .views import SelectViews



urlpatterns = [
    path('',views.index),
    path('login/',views.doLogin),
    path('chat',views.chat,name='chat'),
    path('contact',views.contact),
    path('register',views.register),
    path('forgotpswd/',views.forgotpswd),
    path('logout/',views.logout),
    path('generate_random_password',views.generate_random_password),
    path('reset_password',views.reset_password,name='password_change'),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),
    path('password_change_form',views.change_password),
    path('financial_services.html', views.financial_services, name='financial_services'),
    
# Views updateview, listview, createview
    path('model_list', MyModelListView.as_view(), name='model_list'),
    path('model_update/<int:pk>/', MyModelUpdateView.as_view(), name='model_update'),
    path('model_create', MyModelCreateView.as_view(), name='model_create'),
    # path('shop_reg/', ShopRegistrationView.as_view(), name='shop_reg'),
    # path('approve_shop/', ApproveShopView.as_view(), name='approve_shops'),
    # path('approve/<int:user_id>/', ApproveShopView.as_view(), name='approve_shop_action'),  
    path('page/', SelectViews.as_view(), name='selectview'), 
    
    
]
