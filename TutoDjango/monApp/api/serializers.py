from rest_framework import serializers
from monApp.models import Categorie, Produit, Rayon, Statut, Contenir
from datetime import datetime



class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ["refProd", "intituleProd", "prixUnitaireProd", "dateFabProd", "categorie"]

class CategorieSerializer(serializers.ModelSerializer):
    produits_categorie = serializers.SerializerMethodField()
    class Meta:
        model = Categorie
        fields = ["idCat", "nomCat", "produits_categorie"]

    def get_produits_categorie(self,instance):
        queryset = instance.produits_categorie.all()
        # Ne renvoyer les produits que si la catégorie en a au moins 2
        if queryset.count() < 2:
            return [] # moins de 2 produits → on renvoie une liste vide
        serializer = ProduitSerializer(queryset, many=True)
        return serializer.data

class RayonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rayon
        fields = ["idRayon", "nomRayon"]

class StatutSerializer(serializers.ModelSerializer):
    produits_status = ProduitSerializer(many=True)
    class Meta:
        model = Statut
        fields = ["idStatus", "libelleStatus", "produits_status"]

class ContenirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenir
        fields = ["produit", "rayon", "Qte"]