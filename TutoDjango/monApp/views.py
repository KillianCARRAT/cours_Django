from django.shortcuts import render
from .models import Produit, Categorie, Statut, Rayon

# Create your views here.
from django.http import HttpResponse, Http404

def home(request, param=""):
    return HttpResponse("<h1>Hello " + ("Django" if param == "" else param) + "!</h1>")


def contact(request):
    return render(request, 'monApp/contact.html')

def about(request):
    return render(request, 'monApp/about.html')

def listProduits(request):
    return render(request, 'monApp/list_produits.html', {'produits': Produit.objects.all()})

def listCategories(request):
    return render(request, 'monApp/list_categorie.html', {'categories': Categorie.objects.all()})

def listStatus(request):
    return render(request, 'monApp/list_statut.html', {'statuts': Statut.objects.all()})

def listRayons(request):
    return render(request, 'monApp/list_rayon.html', {'rayons': Rayon.objects.all()})