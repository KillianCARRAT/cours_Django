from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def homeBase(request):
    return HttpResponse("<h1>Hello Django!</h1>")

def home(request, param):
    return HttpResponse("<h1>Hello " + ("Django" if param == "" else param) + "!</h1>")

def contact(request):
    return HttpResponse("<h1>Contact Us</h1>")

def about(request):
    return HttpResponse("<h1>About Us</h1>")