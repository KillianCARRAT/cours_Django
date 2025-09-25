from django.shortcuts import render, redirect
from .models import Produit, Categorie, Statut, Rayon, Contenir
from .forms import *

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import BaseModelForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.core.mail import send_mail
from django.db.models import Count, Prefetch

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from django.http import HttpResponse, Http404

def listProduits(request):
    return render(request, 'monApp/Read/list/produits.html', {'produits': Produit.objects.all()})

def listCategories(request):
    return render(request, 'monApp/Read/list/categories.html', {'categories': Categorie.objects.all()})

def listStatus(request):
    return render(request, 'monApp/Read/list/statuts.html', {'statuts': Statut.objects.all()})

def listRayons(request):
    return render(request, 'monApp/Read/list/rayons.html', {'rayons': Rayon.objects.all()})


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


def ContactView(request):
    titreh1 = "Contact us !"
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request, "monApp/page_home.html", {'titreh1': titreh1, 'form': form})

class EmailSentView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(EmailSentView, self).get_context_data(**kwargs)
        context['titreh1'] = "Contact"
        context['message'] = "E-mail envoyé avec succès"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)


class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/Read/list/produits.html"
    context_object_name = "produits"

    def get_queryset(self):
        return Produit.objects.select_related('categorie').select_related('status').order_by("prixUnitaireProd")

    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context

class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/Read/detail/produit.html"
    context_object_name = "prdt"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context


class CategorieListView(ListView):
    model = Categorie
    template_name = "monApp/Read/list/categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))

    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context

class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/Read/detail/categorie.html"
    context_object_name = "categorie"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))

    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du catégorie"
        context['prdts'] = self.object.produits_categorie.all()
        return context

class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/Read/list/rayons.html"
    context_object_name = "rayons"

    def get_queryset(self):
        # Précharge tous les "contenir" de chaque rayon,
        # et en même temps le produit de chaque contenir
        return Rayon.objects.prefetch_related(
        Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit"))
        )

    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        ryns_dt = []
        for rayon in context['rayons']:
            total = 0
            for contenir in rayon.contenir_rayon.all():
                total += contenir.produit.prixUnitaireProd * contenir.Qte
            ryns_dt.append({'rayon': rayon,'total_stock': total})
            context['rayons_dt'] = ryns_dt
        return context

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/Read/detail/rayon.html"
    context_object_name = "rayon"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"

        prdts_dt = []
        total_rayon = 0
        total_nb_produit = 0
        for contenir in self.object.contenir_rayon.all():
            total_produit = contenir.produit.prixUnitaireProd * contenir.Qte
            prdts_dt.append({ 'produit': contenir.produit,
                                'qte': contenir.Qte,
                                'prix_unitaire': contenir.produit.prixUnitaireProd,
                                'total_produit': total_produit})
            total_rayon += total_produit
            total_nb_produit += contenir.Qte

        context['prdts_dt'] = prdts_dt
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit

        return context

class StatutListView(ListView):
    model = Statut
    template_name = "monApp/Read/list/statuts.html"
    context_object_name = "statuts"

    def get_queryset(self):
        return Statut.objects.prefetch_related('produits_status').annotate(nb_produits=Count('produits_status'))

    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes statuts"
        return context

class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/Read/detail/statut.html"
    context_object_name = "statut"

    def get_queryset(self):
        return Statut.objects.annotate(nb_produits=Count('produits_status'))

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        context['prdts'] = self.object.produits_status.all()
        return context


class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'

    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')


class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')


class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)

# Views CRUD
# Views CREATE
@method_decorator(login_required, name='dispatch')
class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/Create/produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', pk=prdt.refProd)

@method_decorator(login_required, name='dispatch')
class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "monApp/Create/categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_categorie', pk=cat.idCat)

@method_decorator(login_required, name='dispatch')
class RayonCreateView(CreateView):
    model = Rayon
    form_class = RayonForm
    template_name = "monApp/Create/rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ray = form.save()
        return redirect('dtl_rayon', pk=ray.idRayon)

@method_decorator(login_required, name='dispatch')
class StatutCreateView(CreateView):
    model = Statut
    form_class = StatutForm
    template_name = "monApp/Create/statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_statut', pk=stat.idStatus)


# Views UPDATE
@method_decorator(login_required, name='dispatch')
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/Update/produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)

@method_decorator(login_required, name='dispatch')
class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = "monApp/Update/categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_categorie', pk=cat.idCat)

@method_decorator(login_required, name='dispatch')
class RayonUpdateView(UpdateView):
    model = Rayon
    form_class = RayonForm
    template_name = "monApp/Update/rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ray = form.save()
        return redirect('dtl_rayon', pk=ray.idRayon)

@method_decorator(login_required, name='dispatch')
class StatutUpdateView(UpdateView):
    model = Statut
    form_class = StatutForm
    template_name = "monApp/Update/statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_statut', pk=stat.idStatus)


# Views DELETE
@method_decorator(login_required, name='dispatch')
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/Delete/produit.html"
    success_url = reverse_lazy('lst_prdts')

@method_decorator(login_required, name='dispatch')
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/Delete/categorie.html"
    success_url = reverse_lazy('lst_categories')

@method_decorator(login_required, name='dispatch')
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/Delete/rayon.html"
    success_url = reverse_lazy('lst_rayons')

@method_decorator(login_required, name='dispatch')
class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "monApp/Delete/statut.html"
    success_url = reverse_lazy('lst_statuts')