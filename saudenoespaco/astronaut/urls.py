from django.urls import path
from  . import views

urlpatterns = [
    path('', views.astronaut_index, name='astronaut_index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visor/', views.visor_astronaut, name='visor_astronaut'),

    
]