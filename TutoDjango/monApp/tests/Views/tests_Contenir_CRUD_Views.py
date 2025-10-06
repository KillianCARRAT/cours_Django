from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.models import Contenir, Rayon, Produit
from monApp.views import ContenirCreateView, ContenirUpdateView, ContenirDeleteView


class ContenirCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
    
    def test_contenir_create_view_get(self):
        response = self.client.get(reverse('crt_contenir', args=[1])) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/Create/contenir.html')
    
    def test_contenir_create_view_post_valid(self):
        rayon = Rayon.objects.create(nomRayon="RayonPourTestCreation")
        produit = Produit.objects.create(intituleProd="ProduitPourTestCreation", prixUnitaireProd=20.00, dateFabProd="2023-01-01")
        data = { "produit": produit.refProd, "rayon": rayon.idRayon, "Qte": 5 }
        response = self.client.post(reverse('crt_contenir', args=[rayon.idRayon]), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Contenir.objects.count(), 1)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Contenir.objects.last().Qte, 5)



class ContenirUpdateViewTest(TestCase):
    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="RayonPourTestUpdate")
        self.produit = Produit.objects.create(intituleProd="ProduitPourTestUpdate", prixUnitaireProd=25.00, dateFabProd="2023-01-01")
        self.contenir = Contenir.objects.create(produit=self.produit, rayon=self.rayon, Qte=8)
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_contenir_update_view_get(self):
        response = self.client.get(reverse('contenir_chng', args=[self.contenir.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Update/contenir.html')

    def test_update_view_post_valid(self):
        data = { "produit": self.produit.refProd, "rayon": self.rayon.idRayon, "Qte": 9}
        response = self.client.post(reverse('contenir_chng', args=[self.contenir.id]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.contenir.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.contenir.Qte, 9)

class ContenirDeleteViewTest(TestCase):
    def setUp(self):
        rayon = Rayon.objects.create(nomRayon="RayonPourTestDelete")
        produit = Produit.objects.create(intituleProd="ProduitPourTestDelete", prixUnitaireProd=30.00, dateFabProd="2023-01-01")
        self.contenir = Contenir.objects.create(rayon=rayon, produit=produit, Qte=12)
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_contenir_delete_view_get(self):
        response = self.client.get(reverse('dlt_contenir', args=[self.contenir.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/Delete/contenir.html')

    def test_contenir_delete_view_post(self):
        response = self.client.post(reverse('dlt_contenir', args=[self.contenir.id]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Contenir.objects.filter(pk=self.contenir.id).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_rayons'))