from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from monApp.models import Categorie, Produit, Rayon, Statut, Contenir
from .serializers import CategorieSerializer, ProduitSerializer, RayonSerializer, StatutSerializer, ContenirSerializer
from datetime import datetime

# List and Create
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

# Details
class CategorieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ProduitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class RayonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rayon.objects.all()
    serializer_class = RayonSerializer  

class StatutDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer

class ContenirDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer



class SmallResultsSetPagination(PageNumberPagination):
    page_size = 2 # minimum de résultats par page
    page_size_query_param = 'page_size'
    max_page_size = 4 # maximum de résultats par page

# ViewSets
class CategorieViewSet(viewsets.ModelViewSet):
    # pagination_class = None
    pagination_class = SmallResultsSetPagination
    queryset = Categorie.objects.all().prefetch_related('produits_categorie')
    serializer_class = CategorieSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    # queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def get_queryset(self):
        queryset = Produit.objects.all()
        datefilter = self.request.GET.get('datefilter')
        if datefilter is not None:
            datefilter=datetime.strptime(datefilter, "%d/%m/%Y")
            queryset = queryset.filter(dateFabProd__gt=datefilter)
        return queryset

class RayonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rayon.objects.all()
    serializer_class = RayonSerializer

class StatutViewSet(viewsets.ModelViewSet):
    queryset = Statut.objects.all().prefetch_related("produits_status")
    serializer_class = StatutSerializer

class ContenirViewSet(viewsets.ModelViewSet):
    queryset = Contenir.objects.all()
    serializer_class = ContenirSerializer