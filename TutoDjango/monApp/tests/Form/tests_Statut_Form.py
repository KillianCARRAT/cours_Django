from django.test import TestCase
from monApp.models import Statut
from monApp.forms import StatutForm

class StatutFormTest(TestCase):
    def test_form_valid_data(self):
        form = StatutForm(data = {'libelleStatus': 'RayonPourTest'})
        self.assertTrue(form.is_valid())

    def test_form_valid_data_too_long(self):
        form = StatutForm(data = {'libelleStatus':
        'CategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTestCategoriePourTest'})
        self.assertFalse(form.is_valid())
        self.assertIn('libelleStatus', form.errors)
        self.assertEqual(form.errors['libelleStatus'], ['Assurez-vous que cette valeur comporte au plus 100 caractères (actuellement 102).'])

    def test_form_valid_data_missed(self):
        form = StatutForm(data = {'libelleStatus': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('libelleStatus', form.errors)
        self.assertEqual(form.errors['libelleStatus'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = StatutForm(data = {'libelleStatus': 'CategoriePourTest'})
        self.assertTrue(form.is_valid())
        status = form.save()
        self.assertEqual(status.libelleStatus, 'CategoriePourTest')
        self.assertEqual(status.idStatus, 1)