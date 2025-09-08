from django.urls import path
from . import views

urlpatterns = [
    # Page Home
    path("", views.home, name="home"),
    path('home/<str:param>', views.home, name='home'),

    # Page autre
    path("contact", views.contact, name="contact us"),
    path("about", views.about, name="about us"),

    path("produits", views.listProduits, name="liste produits"),
    path("categories", views.listCategories, name="liste categories"),
    path("status", views.listStatus, name="liste status"),
    path("rayons", views.listRayons, name="liste rayons"),
    

]