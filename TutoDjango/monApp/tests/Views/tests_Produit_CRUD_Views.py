from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Produit
from monApp.views import ProduitListView, ProduitDetailView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView


class ProduitCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
    
    def test_Produit_create_view_get(self):
        response = self.client.get(reverse('crt_prdt')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/Create/produit.html')
    
    def test_Produit_create_view_post_valid(self):
        data = { "intituleProd": "ProduitPourTestCreation", "prixUnitaireProd": 25.00, "dateFabProd": "2023-01-01" }
        response = self.client.post(reverse('crt_prdt'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Produit.objects.count(), 1)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Produit.objects.last().intituleProd, 'ProduitPourTestCreation')


class ProduitDetailViewTest(TestCase):
    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="ProduitPourTestDetail", prixUnitaireProd=10.00, dateFabProd="2023-01-01")
    
    def test_Produit_detail_view(self):
        response = self.client.get(reverse('dtl_prdt', args=[self.produit.refProd]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Read/detail/produit.html')
        # Vérifie que le nom de la Produit est affiché
        self.assertContains(response, 'ProduitPourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

class ProduitUpdateViewTest(TestCase):
    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="ProduitPourTestUpdate", prixUnitaireProd=20.00, dateFabProd="2023-01-01")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_Produit_update_view_get(self):
        response = self.client.get(reverse('prdt_chng', args=[self.produit.refProd]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Update/produit.html')

    def test_update_view_post_valid(self):
        self.assertEqual(self.produit.intituleProd, 'ProduitPourTestUpdate')
        data = {'intituleProd': 'ProduitPourTestAfterUpdate', 'prixUnitaireProd': 20.00, 'dateFabProd': '2023-01-01'}
        response = self.client.post(reverse('prdt_chng', args=[self.produit.refProd]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.produit.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.produit.intituleProd, 'ProduitPourTestAfterUpdate')

class ProduitDeleteViewTest(TestCase):
    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="ProduitPourTesDelete", prixUnitaireProd=30.00, dateFabProd="2023-01-01")
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_Produit_delete_view_get(self):
        response = self.client.get(reverse('dlt_prdt', args=[self.produit.refProd]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Delete/produit.html')

    def test_Produit_delete_view_post(self):
        response = self.client.post(reverse('dlt_prdt', args=[self.produit.refProd]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Produit.objects.filter(refProd=self.produit.refProd).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_prdts'))