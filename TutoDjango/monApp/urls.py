from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    # Page autre
    # path("produits", views.listProduits, name="liste produits"),
    path("categories", views.listCategories, name="liste categories"),
    path("status", views.listStatus, name="liste status"),
    path("rayons", views.listRayons, name="liste rayons"),

    # Vue Généric
    path("home", TemplateView.as_view(template_name="monApp/page_home.html")),
    path("home/", views.HomeView.as_view()),
    path("home/<str:param>", views.HomeView.as_view()),

    path("about/", views.AboutView.as_view()),
    path("contact/", views.ContactView.as_view()),

    path("produits/",views.ProduitListView.as_view()),
    

]