from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Rayon
from monApp.views import RayonListView, RayonDetailView, RayonCreateView, RayonUpdateView, RayonDeleteView

class RayonUrlsTest(TestCase):
    def test_rayon_list_url_is_resolved(self):
        url = reverse('lst_rayons')
        self.assertEqual(resolve(url).view_name, 'lst_rayons')
        self.assertEqual(resolve(url).func.view_class, RayonListView)

    def test_rayon_detail_url_is_resolved(self):
        url = reverse('dtl_rayon', args=[1])
        self.assertEqual(resolve(url).view_name, 'dtl_rayon')
        self.assertEqual(resolve(url).func.view_class, RayonDetailView)

    def test_rayon_create_url_is_resolved(self):
        url = reverse('crt_rayon')
        self.assertEqual(resolve(url).view_name, 'crt_rayon')
        self.assertEqual(resolve(url).func.view_class, RayonCreateView)

    def test_rayon_update_url_is_resolved(self):
        url = reverse('rayon_chng', args=[1])
        self.assertEqual(resolve(url).view_name, 'rayon_chng')
        self.assertEqual(resolve(url).func.view_class, RayonUpdateView)

    def test_rayon_delete_url_is_resolved(self):
        url = reverse('dlt_rayon', args=[1])
        self.assertEqual(resolve(url).view_name, 'dlt_rayon')
        self.assertEqual(resolve(url).func.view_class, RayonDeleteView)

    def test_rayon_list_response_code(self):
        response = self.client.get(reverse('lst_rayons'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="rayonPourTest")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_rayon_detail_response_code(self):
        url = reverse('dtl_rayon', args=[self.rayon.idRayon]) # idRayon existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rayon_create_response_code_OK(self):
        response = self.client.get(reverse('crt_rayon'))
        self.assertEqual(response.status_code, 200)

    def test_rayon_detail_response_code_KO(self):
        url = reverse('dtl_rayon', args=[9999]) # idRayon non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_rayon_update_response_code_OK(self):
        url = reverse('rayon_chng', args=[self.rayon.idRayon]) # idRayon existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rayon_update_response_code_KO(self):
        url = reverse('rayon_chng', args=[9999]) # idRayon non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_rayon_delete_response_code_OK(self):
        url = reverse('dtl_rayon', args=[self.rayon.idRayon]) # idRayon existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rayon_delete_response_code_KO(self):
        url = reverse('dtl_rayon', args=[9999]) # idRayon non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_after_rayon_creation(self):
        response = self.client.post(reverse('crt_rayon'), {'nomRayon': 'RayonPourTestRedirectionCreation'})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monApp/rayon/2/')

    def test_redirect_after_rayon_updating(self):
        response = self.client.post(
            reverse('rayon_chng', args=[self.rayon.idRayon]),
            data={"nomRayon": "RayonPourTestRedirectionMaj"}
        )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f'/monApp/rayon/{self.rayon.idRayon}/')

    def test_redirect_after_rayon_deletion(self):
        response = self.client.post(reverse('dlt_rayon', args=[self.rayon.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lst_rayons'))
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Rayon.objects.filter(pk=self.rayon.pk).exists())