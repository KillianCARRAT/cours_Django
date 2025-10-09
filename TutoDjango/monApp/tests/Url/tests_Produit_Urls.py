from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Produit
from monApp.views import ProduitListView, ProduitDetailView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView

class ProduitUrlsTest(TestCase):
    def test_produit_list_url_is_resolved(self):
        url = reverse('lst_prdts')
        self.assertEqual(resolve(url).view_name, 'lst_prdts')
        self.assertEqual(resolve(url).func.view_class, ProduitListView)

    def test_produit_detail_url_is_resolved(self):
        url = reverse('dtl_prdt', args=[1])
        self.assertEqual(resolve(url).view_name, 'dtl_prdt')
        self.assertEqual(resolve(url).func.view_class, ProduitDetailView)

    def test_produit_create_url_is_resolved(self):
        url = reverse('crt_prdt')
        self.assertEqual(resolve(url).view_name, 'crt_prdt')
        self.assertEqual(resolve(url).func.view_class, ProduitCreateView)

    def test_produit_update_url_is_resolved(self):
        url = reverse('prdt_chng', args=[1])
        self.assertEqual(resolve(url).view_name, 'prdt_chng')
        self.assertEqual(resolve(url).func.view_class, ProduitUpdateView)

    def test_produit_delete_url_is_resolved(self):
        url = reverse('dlt_prdt', args=[1])
        self.assertEqual(resolve(url).view_name, 'dlt_prdt')
        self.assertEqual(resolve(url).func.view_class, ProduitDeleteView)

    def test_produit_list_response_code(self):
        response = self.client.get(reverse('lst_prdts'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.produit = Produithome.objects.create(intituleProd="ProduitPourTest", prixUnitaireProd=10.00, dateFabProd="2023-01-01")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_produit_detail_response_code(self):
        url = reverse('dtl_prdt', args=[self.produit.refProd]) # refProd existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_produit_create_response_code_OK(self):
        response = self.client.get(reverse('crt_prdt'))
        self.assertEqual(response.status_code, 200)

    def test_produit_detail_response_code_KO(self):
        url = reverse('dtl_prdt', args=[9999]) # refProd non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_produit_update_response_code_OK(self):
        url = reverse('prdt_chng', args=[self.produit.refProd]) # refProd existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_produit_update_response_code_KO(self):
        url = reverse('prdt_chng', args=[9999]) # refProd non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_produit_delete_response_code_OK(self):
        url = reverse('dtl_prdt', args=[self.produit.refProd]) # refProd existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_produit_delete_response_code_KO(self):
        url = reverse('dtl_prdt', args=[9999]) # refProd non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_after_Produit_creation(self):
        response = self.client.post(reverse('crt_prdt'), {'intituleProd': 'ProduitPourTestRedirectionCreation', 'prixUnitaireProd': 15.00, 'dateFabProd': '2023-01-01'})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monApp/produit/2/')

    def test_redirect_after_Produit_updating(self):
        response = self.client.post(
            reverse('prdt_chng', args=[self.produit.refProd]),
            data={"intituleProd": "ProduitPourTestRedirectionMaj", "prixUnitaireProd": 20.00, "dateFabProd": "2023-01-01"}
        )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f'/monApp/produit/{self.produit.refProd}/')

    def test_redirect_after_Produit_deletion(self):
        response = self.client.post(reverse('dlt_prdt', args=[self.produit.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lst_prdts'))
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Produit.objects.filter(pk=self.produit.pk).exists())