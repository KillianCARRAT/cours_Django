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

class CategorieSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["idCat", "nomCat"]

class RayonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rayon
        fields = ["idRayon", "nomRayon"]

class StatusSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Statut
        fields = ["idStatus", "libelleStatus"]

class StatusSerializer(serializers.ModelSerializer):
    produits_status = serializers.SerializerMethodField()

    class Meta:
        model = Statut
        fields = ["idStatus", "libelleStatus", "produits_status"]

    def get_produits_status(self,instance):
        queryset = instance.produits_status.all()
        serializer = ProduitSerializer(queryset, many=True)
        return serializer.data

class ContenirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenir
        fields = ["produit", "rayon", "Qte"]


class MultipleSerializerMixin:
    detail_serializer_class = None
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()