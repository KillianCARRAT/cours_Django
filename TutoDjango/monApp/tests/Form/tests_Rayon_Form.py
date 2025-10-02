from django.test import TestCase
from monApp.models import Rayon
from monApp.forms import RayonForm

class RayonFormTest(TestCase):
    def test_form_valid_data(self):
        form = RayonForm(data = {'nomRayon': 'RayonPourTest'})
        self.assertTrue(form.is_valid())

    def test_form_valid_data_too_long(self):
        form = RayonForm(data = {'nomRayon':
        'CategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTest'})
        self.assertFalse(form.is_valid())
        self.assertIn('nomRayon', form.errors)
        self.assertEqual(form.errors['nomRayon'], ['Assurez-vous que cette valeur comporte au plus 100 caractères (actuellement 102).'])

    def test_form_valid_data_missed(self):
        form = RayonForm(data = {'nomRayon': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('nomRayon', form.errors)
        self.assertEqual(form.errors['nomRayon'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = RayonForm(data = {'nomRayon': 'CategoriePourTest'})
        self.assertTrue(form.is_valid())
        rayon = form.save()
        self.assertEqual(rayon.nomRayon, 'CategoriePourTest')
        self.assertEqual(rayon.idRayon, 1)