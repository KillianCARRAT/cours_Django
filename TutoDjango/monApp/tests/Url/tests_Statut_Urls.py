from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Statut
from monApp.views import StatutListView, StatutDetailView, StatutCreateView, StatutUpdateView, StatutDeleteView

class StatutUrlsTest(TestCase):
    def test_statut_list_url_is_resolved(self):
        url = reverse('lst_statuts')
        self.assertEqual(resolve(url).view_name, 'lst_statuts')
        self.assertEqual(resolve(url).func.view_class, StatutListView)

    def test_statut_detail_url_is_resolved(self):
        url = reverse('dtl_statut', args=[1])
        self.assertEqual(resolve(url).view_name, 'dtl_statut')
        self.assertEqual(resolve(url).func.view_class, StatutDetailView)

    def test_statut_create_url_is_resolved(self):
        url = reverse('crt_statut')
        self.assertEqual(resolve(url).view_name, 'crt_statut')
        self.assertEqual(resolve(url).func.view_class, StatutCreateView)

    def test_statut_update_url_is_resolved(self):
        url = reverse('statut_chng', args=[1])
        self.assertEqual(resolve(url).view_name, 'statut_chng')
        self.assertEqual(resolve(url).func.view_class, StatutUpdateView)

    def test_statut_delete_url_is_resolved(self):
        url = reverse('dlt_statut', args=[1])
        self.assertEqual(resolve(url).view_name, 'dlt_statut')
        self.assertEqual(resolve(url).func.view_class, StatutDeleteView)

    def test_statut_list_response_code(self):
        response = self.client.get(reverse('lst_statuts'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.statut = Statut.objects.create(libelleStatus="StatutPourTest")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_statut_detail_response_code(self):
        url = reverse('dtl_statut', args=[self.statut.idStatus]) # idStatus existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_statut_create_response_code_OK(self):
        response = self.client.get(reverse('crt_statut'))
        self.assertEqual(response.status_code, 200)

    def test_statut_detail_response_code_KO(self):
        url = reverse('dtl_statut', args=[9999]) # idStatus non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_statut_update_response_code_OK(self):
        url = reverse('statut_chng', args=[self.statut.idStatus]) # idStatus existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_statut_update_response_code_KO(self):
        url = reverse('statut_chng', args=[9999]) # idStatus non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_statut_delete_response_code_OK(self):
        url = reverse('dtl_statut', args=[self.statut.idStatus]) # idStatus existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_statut_delete_response_code_KO(self):
        url = reverse('dtl_statut', args=[9999]) # idStatus non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_after_Statut_creation(self):
        response = self.client.post(reverse('crt_statut'), {'libelleStatus': 'StatutPourTestRedirectionCreation'})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monApp/statut/2/')

    def test_redirect_after_Statut_updating(self):
        response = self.client.post(
            reverse('statut_chng', args=[self.statut.idStatus]),
            data={"libelleStatus": "StatutPourTestRedirectionMaj"}
        )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f'/monApp/statut/{self.statut.idStatus}/')

    def test_redirect_after_Statut_deletion(self):
        response = self.client.post(reverse('dlt_statut', args=[self.statut.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lst_statuts'))
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Statut.objects.filter(pk=self.statut.pk).exists())