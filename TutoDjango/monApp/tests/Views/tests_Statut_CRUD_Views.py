from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Statut
from monApp.views import StatutListView, StatutDetailView, StatutCreateView, StatutUpdateView, StatutDeleteView


class StatutCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
    
    def test_statut_create_view_get(self):
        response = self.client.get(reverse('crt_statut')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/Create/statut.html')
    
    def test_statut_create_view_post_valid(self):
        data = { "libelleStatus": "StatutPourTestCreation" }
        response = self.client.post(reverse('crt_statut'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Statut.objects.count(), 1)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Statut.objects.last().libelleStatus, 'StatutPourTestCreation')


class StatutDetailViewTest(TestCase):
    def setUp(self):
        self.statut = Statut.objects.create(libelleStatus="StatutPourTestDetail")
    
    def test_statut_detail_view(self):
        response = self.client.get(reverse('dtl_statut', args=[self.statut.idStatus]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Read/detail/statut.html')
        # Vérifie que le nom de la Statut est affiché
        self.assertContains(response, 'StatutPourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

class StatutUpdateViewTest(TestCase):
    def setUp(self):
        self.statut = Statut.objects.create(libelleStatus="StatutPourTestUpdate")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_statut_update_view_get(self):
        response = self.client.get(reverse('statut_chng', args=[self.statut.idStatus]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Update/statut.html')

    def test_update_view_post_valid(self):
        self.assertEqual(self.statut.libelleStatus, 'StatutPourTestUpdate')
        data = {'libelleStatus': 'StatutPourTestAfterUpdate'}
        response = self.client.post(reverse('statut_chng', args=[self.statut.idStatus]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.statut.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.statut.libelleStatus, 'StatutPourTestAfterUpdate')

class StatutDeleteViewTest(TestCase):
    def setUp(self):
        self.statut = Statut.objects.create(libelleStatus="StatutPourTesDelete")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_statut_delete_view_get(self):
        response = self.client.get(reverse('dlt_statut', args=[self.statut.idStatus]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Delete/statut.html')

    def test_statut_delete_view_post(self):
        response = self.client.post(reverse('dlt_statut', args=[self.statut.idStatus]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Statut.objects.filter(idStatus=self.statut.idStatus).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_statuts'))