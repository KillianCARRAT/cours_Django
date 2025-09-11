from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    # Vue Généric
    path("home", TemplateView.as_view(template_name="monApp/page_home.html")),
    path("home/", views.HomeView.as_view()),
    path("home/<str:param>", views.HomeView.as_view()),

    path("about/", views.AboutView.as_view()),
    path("contact/", views.ContactView.as_view()),

    path("produits/",views.ProduitListView.as_view(), name="lst_prdts"),
    path("produit/<int:pk>/",views.ProduitDetailView.as_view(), name="dtl_prdt"),

    # path("categories/",views..as_view(), name="lst_categories"),
    # path("produit/<int:pk>/",views..as_view(), name="dtl_categorie"),

    # path("rayons/",views..as_view(), name="lst_rayons"),
    # path("rayon/<int:pk>/",views..as_view(), name="dtl_rayon"),

    # path("statuts/",views..as_view(), name="lst_statuts"),
    # path("statut/<int:pk>/",views..as_view(), name="dtl_statut"),
    

]