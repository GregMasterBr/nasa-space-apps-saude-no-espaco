from django.urls import path
from  . import views

urlpatterns = [
    path('', views.home_analytics, name='home_analytics'),
]