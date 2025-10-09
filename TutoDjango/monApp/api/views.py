from rest_framework import generics
from monApp.models import Categorie, Produit, Rayon, Statut, Contenir
from .serializers import CategorieSerializer, ProduitSerializer, RayonSerializer, StatutSerializer, ContenirSerializer

class CategorieAPIView(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ProduitAPIView(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class RayonAPIView(generics.ListCreateAPIView):
    queryset = Rayon.objects.all()
    serializer_class = RayonSerializer

class StatutAPIView(generics.ListCreateAPIView):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer

class ContenirAPIView(generics.ListCreateAPIView):
    queryset = Contenir.objects.all()
    serializer_class = ContenirSerializer