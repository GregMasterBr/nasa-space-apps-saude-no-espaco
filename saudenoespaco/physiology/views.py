from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.

def home_physiology(request):
    messages.add_message(request, constants.SUCCESS, 'Página carregada com sucesso')
    return render(request,'index.html')