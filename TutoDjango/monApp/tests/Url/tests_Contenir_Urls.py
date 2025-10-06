from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Produit, Rayon, Contenir
from monApp.views import ContenirCreateView, ContenirUpdateView, ContenirDeleteView

class ContenirUrlsTest(TestCase):
    def test_Contenir_create_url_is_resolved(self):
        url = reverse('crt_contenir', args=[1])
        self.assertEqual(resolve(url).view_name, 'crt_contenir')
        self.assertEqual(resolve(url).func.view_class, ContenirCreateView)

    def test_Contenir_update_url_is_resolved(self):
        url = reverse('contenir_chng', args=[1])
        self.assertEqual(resolve(url).view_name, 'contenir_chng')
        self.assertEqual(resolve(url).func.view_class, ContenirUpdateView)

    def test_Contenir_delete_url_is_resolved(self):
        url = reverse('dlt_contenir', args=[1])
        self.assertEqual(resolve(url).view_name, 'dlt_contenir')
        self.assertEqual(resolve(url).func.view_class, ContenirDeleteView)

    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="ProduitPourTest", prixUnitaireProd=10.00, dateFabProd="2023-01-01")
        self.rayon = Rayon.objects.create(nomRayon="RayonPourTest")
        self.contenir = Contenir.objects.create(produit=self.produit, rayon=self.rayon, Qte=5)
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_Contenir_create_response_code_OK(self):
        self.client.get(reverse('crt_prdt'))
        self.client.get(reverse('crt_rayon'))
        response = self.client.get(reverse('crt_contenir', args=[self.rayon.idRayon]))
        self.assertEqual(response.status_code, 200)
    
    def test_Contenir_update_response_code_OK(self):
        url = reverse('contenir_chng', args=[self.contenir.id]) # id existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_Contenir_update_response_code_KO(self):
        url = reverse('contenir_chng', args=[9999]) # id non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_Contenir_delete_response_code_OK(self):
        url = reverse('dtl_prdt', args=[self.contenir.id]) # id existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_Contenir_delete_response_code_KO(self):
        url = reverse('dtl_prdt', args=[9999]) # id non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_after_Contenir_creation(self):
        rayon = Rayon.objects.create(nomRayon="RayonPourTestRedirect")
        produit = Produit.objects.create(intituleProd="ProduitPourTestRedirect", prixUnitaireProd=15.00, dateFabProd="2023-01-02")
        response = self.client.post(reverse('crt_contenir', args=[rayon.idRayon]), 
                                data={"produit": produit.refProd, "rayon": rayon.idRayon, "Qte": 10})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monApp/rayon/2/')

    def test_redirect_after_Contenir_updating(self):
        response = self.client.post(
            reverse('contenir_chng', args=[self.contenir.id]),
            data={"produit": self.produit.refProd, "rayon": self.rayon.idRayon, "Qte": 20}
        )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f'/monApp/rayon/{self.rayon.idRayon}/')

    def test_redirect_after_Contenir_deletion(self):
        response = self.client.post(reverse('dlt_contenir', args=[self.contenir.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lst_rayons'))
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Contenir.objects.filter(pk=self.contenir.pk).exists())