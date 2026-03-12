
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expense.urls')),
    path('', include('income.urls')),
    path('', include('budget.urls')),
    path('', include('income_tracking.urls')),
    path('', include('user.urls')),
    path('', include('admin_app.urls')),
    
]
