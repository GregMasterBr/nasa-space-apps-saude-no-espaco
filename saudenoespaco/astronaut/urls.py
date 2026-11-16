
from django.urls import path
from . import views

urlpatterns = [
    path('', views.astronaut_index, name='astronaut_index'),
    path('conversation/', views.fake, name='fake'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('visor/', views.visor_astronaut, name='visor_astronaut'),

    # Family Communication
    path(
        'communication/<int:astronaut_id>/',
        views.family_communication,
        name='family_communication'
    ),

    path(
        'communication/<int:astronaut_id>/call/<int:call_id>/',
        views.communication_call,
        name='communication_call'
    ),

    path(
        'communication/<int:astronaut_id>/history/',
        views.communication_history,
        name='communication_history'
    ),
]
