from django.test import TestCase
from monApp.models import Contenir, Produit, Rayon

class ProduitModelTest(TestCase):

    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="ProdTestContenir", prixUnitaireProd=10.00, dateFabProd="2023-10-10")
        self.rayon = Rayon.objects.create(nomRayon="TestContenir")
        self.contenir = Contenir.objects.create(produit=self.produit, rayon=self.rayon, Qte=5)
    
    def test_categorie_creation(self):
        self.assertEqual(self.contenir.produit.intituleProd, "ProdTestContenir")
        self.assertEqual(self.contenir.rayon.nomRayon, "TestContenir")
        self.assertEqual(self.contenir.Qte, 5)

    def test_string_representation(self):
        self.assertEqual(str(self.contenir), f"{self.contenir.produit.intituleProd} dans {self.contenir.rayon.nomRayon} (Qte: {self.contenir.Qte})")

    def test_categorie_updating(self):
        self.contenir.Qte = 7
        self.contenir.save()
        updated_Contenir = Contenir.objects.get(id=self.contenir.id)
        self.assertEqual(updated_Contenir.Qte, 7)

    def test_categorie_deletion(self):
        self.contenir.delete()
        self.assertEqual(Contenir.objects.count(), 0)