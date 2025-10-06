from django.test import TestCase
from monApp.models import Produit

class ProduitModelTest(TestCase):

    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="CategoriePourTest", prixUnitaireProd=10.00, dateFabProd="2023-10-10")
    
    def test_categorie_creation(self):
        self.assertEqual(self.produit.intituleProd, "CategoriePourTest")
        self.assertEqual(self.produit.prixUnitaireProd, 10.00)
        self.assertEqual(str(self.produit.dateFabProd), "2023-10-10")

    def test_string_representation(self):
        self.assertEqual(str(self.produit), "CategoriePourTest")

    def test_categorie_updating(self):
        self.produit.intituleProd = "CategoriePourTestTest"
        self.produit.save()
        updated_Produit = Produit.objects.get(refProd=self.produit.refProd)
        self.assertEqual(updated_Produit.intituleProd, "CategoriePourTestTest")

    def test_categorie_deletion(self):
        self.produit.delete()
        self.assertEqual(Produit.objects.count(), 0)