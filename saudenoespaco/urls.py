"""project_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),
    # Página inicial
    path('', include('saudenoespaco.core.urls')),
     # Aplicativos do MINDSPACE
    path('accounts/', include('saudenoespaco.accounts.urls')),
    path('astronaut/', include('saudenoespaco.astronaut.urls')),
    path('analytics/', include('saudenoespaco.analytics.urls')),
    path('interventions/', include('saudenoespaco.interventions.urls')),
    path('medical/', include('saudenoespaco.medical.urls')),
    path('monitoring/', include('saudenoespaco.monitoring.urls')),
    path('physiology/', include('saudenoespaco.physiology.urls')),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)