from django.db import models
from django.db.models.functions import Now

class Categorie(models.Model):
	idCat = models.AutoField(primary_key=True)
	nomCat = models.CharField(max_length=100)

	def __str__(self):
		return self.nomCat

class Status(models.Model):
	idStatus = models.AutoField(primary_key=True)
	libelle = models.CharField(max_length=200)

	def __str__(self):
		return self.libelle

class Produit(models.Model):
	refProd = models.AutoField(primary_key=True)
	intituleProd = models.CharField(max_length=200)
	prixUnitaireProd = models.DecimalField(max_digits=10, decimal_places=2)
	dateFab = models.DateTimeField(db_default=Now())
	# Relation CIF : chaque produit appartient à 1 catégorie (0,N côté catégorie 1,1 côté produit)→
	categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="categorie_produits", null=True, blank=True)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="produits_status", null=True, blank=True)

	def __str__(self):
		return self.intituleProd


class Rayon(models.Model):
	idRayon = models.AutoField(primary_key=True)
	nomRayon = models.CharField(max_length=200)

	def __str__(self):
		return self.nomRayon

class Contenir(models.Model):
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="contient_produit", null=False, blank=True)
	rayon = models.ForeignKey(Rayon, on_delete=models.CASCADE, related_name="rayon_contient", null=False, blank=True)
	qte = models.IntegerField()

	def __str__(self):
		return self.rayon.__str__() + " contient " + self.qte + " " + self.produit.__str__()

