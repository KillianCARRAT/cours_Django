from rest_framework import serializers
from monApp.models import Categorie, Produit, Rayon, Statut, Contenir

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["idCat", "nomCat"]

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ["refProd", "intituleProd", "prixUnitaireProd", "dateFabProd", "categorie"]

class RayonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rayon
        fields = ["idRayon", "nomRayon"]

class StatutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statut
        fields = ["idStatut", "descriptionStatut"]

class ContenirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenir
        fields = ["id", "produit", "rayon", "quantite"]