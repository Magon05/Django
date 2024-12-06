from django.shortcuts import render
from django.views.generic import ListView
from .models import *


class Main(ListView):
    model = personal_data
    template_name = 'profile.html'
