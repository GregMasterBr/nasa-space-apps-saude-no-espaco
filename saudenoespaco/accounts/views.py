from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.

def home_accounts(request):
    return render(request,'accounts_index.html')