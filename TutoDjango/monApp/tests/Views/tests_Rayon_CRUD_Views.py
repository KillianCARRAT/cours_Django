from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Rayon
from monApp.views import RayonListView, RayonDetailView, RayonCreateView, RayonUpdateView, RayonDeleteView


class RayonCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
    
    def test_rayon_create_view_get(self):
        response = self.client.get(reverse('crt_rayon')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/Create/rayon.html')
    
    def test_rayon_create_view_post_valid(self):
        data = { "nomRayon": "RayonPourTestCreation" }
        response = self.client.post(reverse('crt_rayon'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Rayon.objects.count(), 1)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Rayon.objects.last().nomRayon, 'RayonPourTestCreation')


class RayonDetailViewTest(TestCase):
    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="RayonPourTestDetail")
    
    def test_rayon_detail_view(self):
        response = self.client.get(reverse('dtl_rayon', args=[self.rayon.idRayon]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Read/detail/rayon.html')
        # Vérifie que le nom de la Rayon est affiché
        self.assertContains(response, 'RayonPourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

class RayonUpdateViewTest(TestCase):
    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="RayonPourTestUpdate")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_rayon_update_view_get(self):
        response = self.client.get(reverse('rayon_chng', args=[self.rayon.idRayon]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Update/rayon.html')

    def test_update_view_post_valid(self):
        self.assertEqual(self.rayon.nomRayon, 'RayonPourTestUpdate')
        data = {'nomRayon': 'RayonPourTestAfterUpdate'}
        response = self.client.post(reverse('rayon_chng', args=[self.rayon.idRayon]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.rayon.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.rayon.nomRayon, 'RayonPourTestAfterUpdate')

class RayonDeleteViewTest(TestCase):
    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="RayonPourTesDelete")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_rayon_delete_view_get(self):
        response = self.client.get(reverse('dlt_rayon', args=[self.rayon.idRayon]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Delete/rayon.html')

    def test_rayon_delete_view_post(self):
        response = self.client.post(reverse('dlt_rayon', args=[self.rayon.idRayon]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Rayon.objects.filter(idRayon=self.rayon.idRayon).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_rayons'))