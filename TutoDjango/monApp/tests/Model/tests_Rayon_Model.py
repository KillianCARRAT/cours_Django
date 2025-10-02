from django.test import TestCase
from monApp.models import Rayon

class RayonModelTest(TestCase):

    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="CategoriePourTest")
    
    def test_categorie_creation(self):
        self.assertEqual(self.rayon.nomRayon, "CategoriePourTest")

    def test_string_representation(self):
        self.assertEqual(str(self.rayon), "CategoriePourTest")

    def test_categorie_updating(self):
        self.rayon.nomRayon = "CategoriePourTestTest"
        self.rayon.save()
        updated_rayon = Rayon.objects.get(idRayon=self.rayon.idRayon)
        self.assertEqual(updated_rayon.nomRayon, "CategoriePourTestTest")

    def test_categorie_deletion(self):
        self.rayon.delete()
        self.assertEqual(Rayon.objects.count(), 0)