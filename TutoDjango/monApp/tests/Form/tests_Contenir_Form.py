from django.test import TestCase
from monApp.models import Rayon, Produit, Contenir
from monApp.forms import ContenirForm, RayonForm, ProduitForm

class RayonFormTest(TestCase):
    def setUp(self):
        formR = RayonForm(data = {'nomRayon': 'CategoriePourTest'})
        rayon = formR.save()
        formP = ProduitForm(data = {'intituleProd': 'CategoriePourTest', 'prixUnitaireProd': 10.5, 'dateFabProd': '2023-01-01'})
        produit = formP.save()

    def test_form_valid_data(self):
        form = ContenirForm(data = {'produit': 1, 'Qte': 5, 'rayon': 1})
        self.assertTrue(form.is_valid())

    def test_form_valid_data_missed(self):
        form = ContenirForm(data = {'produit': '', 'Qte': '', 'rayon': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('produit', form.errors)
        self.assertEqual(form.errors['produit'], ['Ce champ est obligatoire.'])
        self.assertIn('Qte', form.errors)
        self.assertEqual(form.errors['Qte'], ['Ce champ est obligatoire.'])
        self.assertIn('rayon', form.errors)
        self.assertEqual(form.errors['rayon'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = ContenirForm(data = {'produit': 1, 'Qte': 5, 'rayon': 1})
        self.assertTrue(form.is_valid())
        contenir = form.save()
        self.assertEqual(contenir.produit.refProd, 1)
        self.assertEqual(contenir.Qte, 5)
        self.assertEqual(contenir.rayon.idRayon, 1)
