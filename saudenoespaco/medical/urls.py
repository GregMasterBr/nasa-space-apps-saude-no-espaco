from django.urls import path
from  . import views

urlpatterns = [
    path('', views.home_medical, name='home_medical'),
]