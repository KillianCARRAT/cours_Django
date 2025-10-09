from monApp.api import views
from django.urls import path

urlpatterns = [
    path('categories/',views.CategorieAPIView.as_view(),name="api-lst-ctgrs"),
    path('produits/',views.ProduitAPIView.as_view(),name="api-lst-prdts"),
    path('rayons/',views.RayonAPIView.as_view(),name="api-lst-rayons"),
    path('statuts/',views.StatutAPIView.as_view(),name="api-lst-statuts"),
    path('contenir/',views.ContenirAPIView.as_view(),name="api-lst-contenir"),
]