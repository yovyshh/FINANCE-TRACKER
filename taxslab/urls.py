from django.urls import path
from . import views

urlpatterns = [
    path('add_tax_slab/', views.add_tax_slab, name='add_tax_slab'),  # URL to add a tax slab
    path('tax_slab_list/', views.tax_slab_list, name='tax_slab_list'),  # URL to display tax slabs
]
