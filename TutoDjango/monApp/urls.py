from django.urls import path, include
from . import views
from django.views.generic import *

urlpatterns = [
        # Vue Généric
        path("home", TemplateView.as_view(template_name="monApp/page_home.html")), # pas test
        path("home/", views.HomeView.as_view(), name="home"),
        path("home/<str:param>", views.HomeView.as_view(), name="home_with_param"),

        path("about/", views.AboutView.as_view(), name="about"),
        path("contact/", views.ContactView, name="contact"),
        path("email-sent/", views.EmailSentView.as_view(), name="email-sent"),

        # Produit
        path("produits/", views.ProduitListView.as_view(), name="lst_prdts"),
        path("produit/<int:pk>/", views.ProduitDetailView.as_view(), name="dtl_prdt"),
        path("produit/", views.ProduitCreateView.as_view(), name="crt_prdt"),
        path("produit/<int:pk>/update/", views.ProduitUpdateView.as_view(), name="prdt_chng"),
        path("produit/<int:pk>/delete/", views.ProduitDeleteView.as_view(), name="dlt_prdt"),

        # Categorie
        path("categories/", views.CategorieListView.as_view(), name="lst_categories"),
        path("categories/<int:pk>/", views.CategorieDetailView.as_view(), name="dtl_categorie"),
        path("categorie/", views.CategorieCreateView.as_view(), name="crt_categorie"),
        path("categorie/<int:pk>/update/", views.CategorieUpdateView.as_view(), name="categorie_chng"),
        path("categorie/<int:pk>/delete/", views.CategorieDeleteView.as_view(), name="dlt_categorie"),

        # Rayon
        path("rayons/", views.RayonListView.as_view(), name="lst_rayons"),
        path("rayon/<int:pk>/", views.RayonDetailView.as_view(), name="dtl_rayon"),
        path("rayon/", views.RayonCreateView.as_view(), name="crt_rayon"),
        path("rayon/<int:pk>/update/", views.RayonUpdateView.as_view(), name="rayon_chng"),
        path("rayon/<int:pk>/delete/", views.RayonDeleteView.as_view(), name="dlt_rayon"),

        # Statut
        path("statuts/", views.StatutListView.as_view(), name="lst_statuts"),
        path("statut/<int:pk>/", views.StatutDetailView.as_view(), name="dtl_statut"),
        path("statut/", views.StatutCreateView.as_view(), name="crt_statut"),
        path("statut/<int:pk>/update/", views.StatutUpdateView.as_view(), name="statut_chng"),
        path("statut/<int:pk>/delete/", views.StatutDeleteView.as_view(), name="dlt_statut"),

        # Contenir
        path("rayon/<int:pk>/contenir", views.ContenirCreateView.as_view(), name="crt_contenir"),
        path("contenir/<int:pk>/update/", views.ContenirUpdateView.as_view(), name="contenir_chng"),
        path("contenir/<int:pk>/delete/", views.ContenirDeleteView.as_view(), name="dlt_contenir"),


        # Authentication
        path('login/', views.ConnectView.as_view(), name='login'),
        path('register/', views.RegisterView.as_view(), name='register'),
        path('logout/', views.DisconnectView.as_view(), name='logout'),
        
        # API
        path("api/", include("monApp.api.urls")), # routes API regroupées
]
