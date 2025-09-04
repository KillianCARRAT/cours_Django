from django.shortcuts import render
from .models import Produit, Categorie, Status

# Create your views here.
from django.http import HttpResponse

def home(request, param=""):
    return HttpResponse("<h1>Hello " + ("Django" if param == "" else param) + "!</h1>")

def contact(request):
    return HttpResponse("<h1>Contact Us</h1>")

def about(request):
    return HttpResponse("<h1>About Us</h1>")

def listProduits(request):
    produits = Produit.objects.all()
    prdts = "<ul>"
    for prod in produits:
        prdts += "<li>" + prod.__str__() + "</li>" 
    prdts += "</ul>"
    return HttpResponse("<h1>Liste des porduits</h1>" + prdts)

def listCategories(request):
    categories = Categorie.objects.all()
    cats = "<ul>"
    for cat in categories:
        cats += "<li>" + cat.__str__() + "</li>" 
    cats += "</ul>"
    return HttpResponse("<h1>Liste des categories</h1>" + cats)

def listStatus(request):
    status = Status.objects.all()
    sts = "<ul>"
    for s in status:
        sts += "<li>" + s.__str__() + "</li>" 
    sts += "</ul>"
    return HttpResponse("<h1>Liste des status</h1>" + sts)