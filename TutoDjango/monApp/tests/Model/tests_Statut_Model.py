from django.test import TestCase
from monApp.models import Statut

class StatutModelTest(TestCase):

    def setUp(self):
        self.statut = Statut.objects.create(libelleStatus="CategoriePourTest")
    
    def test_categorie_creation(self):
        self.assertEqual(self.statut.libelleStatus, "CategoriePourTest")

    def test_string_representation(self):
        self.assertEqual(str(self.statut), "CategoriePourTest")

    def test_categorie_updating(self):
        self.statut.libelleStatus = "CategoriePourTestTest"
        self.statut.save()
        updated_statut = Statut.objects.get(idStatus=self.statut.idStatus)
        self.assertEqual(updated_statut.libelleStatus, "CategoriePourTestTest")

    def test_categorie_deletion(self):
        self.statut.delete()
        self.assertEqual(Statut.objects.count(), 0)