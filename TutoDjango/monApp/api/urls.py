from monApp.api import views
from django.urls import path

urlpatterns = [
    path('categories/',views.CategorieAPIView.as_view(),name="api-lst-ctgrs"),
    path('categories/<pk>/',views.CategorieDetailAPIView.as_view(),name="api-dtl-ctgr"),


    path('produits/',views.ProduitAPIView.as_view(),name="api-lst-prdts"),
    path('produits/<pk>/',views.ProduitDetailAPIView.as_view(),name="api-dtl-prdt"),

    path('rayons/',views.RayonAPIView.as_view(),name="api-lst-rayons"),
    path('rayons/<pk>/',views.RayonDetailAPIView.as_view(),name="api-dtl-rayon"),

    path('statuts/',views.StatutAPIView.as_view(),name="api-lst-statuts"),
    path('statuts/<pk>/',views.StatutDetailAPIView.as_view(),name="api-dtl-statut"),

    path('contenir/',views.ContenirAPIView.as_view(),name="api-lst-contenir"),
    path('contenir/<pk>/',views.ContenirDetailAPIView.as_view(),name="api-dtl-contenir"),
]