from django.shortcuts import render
from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = "home/index.html"
    


# Create your views here.