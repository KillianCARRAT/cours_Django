from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    # Vue Généric
    path("home", TemplateView.as_view(template_name="monApp/page_home.html")),
    path("home/", views.HomeView.as_view(), name="home"),
    path("home/<str:param>", views.HomeView.as_view()),

    path("about/", views.AboutView.as_view()),
    path("contact/", views.ContactView, name="contact"),
    path("email-sent/", views.EmailSentView.as_view(), name="email-sent"),

    path("produits/",views.ProduitListView.as_view(), name="lst_prdts"),
    path("produit/<int:pk>/",views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("produit/",views.ProduitCreate, name="crt_prdt"),

    path("categories/",views.CategorieListView.as_view(), name="lst_categories"),
    path("categories/<int:pk>/",views.CategorieDetailView.as_view(), name="dtl_categorie"),

    path("rayons/",views.RayonListView.as_view(), name="lst_rayons"),
    path("rayon/<int:pk>/",views.RayonDetailView.as_view(), name="dtl_rayon"),

    path("statuts/",views.StatutListView.as_view(), name="lst_statuts"),
    path("statut/<int:pk>/",views.StatutDetailView.as_view(), name="dtl_statut"),


    # Authentication
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    

]