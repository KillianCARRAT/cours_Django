from django.test import TestCase
from monApp.models import Produit
from monApp.forms import ProduitForm

class ProduitFormTest(TestCase):
    def test_form_valid_data(self):
        form = ProduitForm(data = {'intituleProd': 'RayonPourTest', 'prixUnitaireProd': 10.5, 'dateFabProd': '2023-01-01'})
        self.assertTrue(form.is_valid())

    def test_form_valid_data_too_long(self):
        form = ProduitForm(data = {'intituleProd':
        'CategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTest',
        'prixUnitaireProd': 10.5, 'dateFabProd': '2023-01-01'})
        self.assertFalse(form.is_valid())
        self.assertIn('intituleProd', form.errors)
        self.assertEqual(form.errors['intituleProd'], ['Assurez-vous que cette valeur comporte au plus 200 caractères (actuellement 204).'])

    def test_form_valid_data_int(self):
        form = ProduitForm(data = {'intituleProd': 'RayonPourTest', 'prixUnitaireProd': 10.555, 'dateFabProd': '2023-01-01'})
        self.assertFalse(form.is_valid())
        self.assertIn('prixUnitaireProd', form.errors)
        self.assertEqual(form.errors['prixUnitaireProd'], ['Assurez-vous qu’il n’y a pas plus de 2 chiffres après la virgule.'])
        form2 = ProduitForm(data = {'intituleProd': 'RayonPourTest', 'prixUnitaireProd': 123456789.5, 'dateFabProd': '2023-01-01'})
        self.assertFalse(form2.is_valid())
        self.assertIn('prixUnitaireProd', form2.errors)
        self.assertEqual(form2.errors['prixUnitaireProd'], ['Assurez-vous qu’il n’y a pas plus de 8 chiffres avant la virgule.'])

    def test_form_valid_data_missed(self):
        form = ProduitForm(data = {'intituleProd': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('intituleProd', form.errors)
        self.assertEqual(form.errors['intituleProd'], ['Ce champ est obligatoire.'])
        self.assertIn('prixUnitaireProd', form.errors)
        self.assertEqual(form.errors['prixUnitaireProd'], ['Ce champ est obligatoire.'])
        self.assertIn('dateFabProd', form.errors)
        self.assertEqual(form.errors['dateFabProd'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = ProduitForm(data = {'intituleProd': 'CategoriePourTest', 'prixUnitaireProd': 10.5, 'dateFabProd': '2023-01-01'})
        self.assertTrue(form.is_valid())
        produit = form.save()
        self.assertEqual(produit.intituleProd, 'CategoriePourTest')
        self.assertEqual(produit.refProd, 1)