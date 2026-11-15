from django.urls import path
from  . import views
from django.contrib.auth import views as auth_views

#app_name = "accounts"

urlpatterns = [
    path('', views.home_accounts, name='home_accounts'),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
]