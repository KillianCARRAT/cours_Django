from django.shortcuts import render
from .models import Produit, Categorie, Statut, Rayon
from django.views.generic import TemplateView

# Create your views here.
from django.http import HttpResponse, Http404

def listProduits(request):
    return render(request, 'monApp/list_produits.html', {'produits': Produit.objects.all()})

def listCategories(request):
    return render(request, 'monApp/list_categorie.html', {'categories': Categorie.objects.all()})

def listStatus(request):
    return render(request, 'monApp/list_statut.html', {'statuts': Statut.objects.all()})

def listRayons(request):
    return render(request, 'monApp/list_rayon.html', {'rayons': Rayon.objects.all()})


# Vue généric
class HomeView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello " + self.kwargs.get('param', 'DJango') + " !"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)

class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)


class ContactView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['titreh1'] = "Contact us..."
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)


class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"