from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import HomeView

from django.test import TestCase
from django.urls import reverse

class HomeViewTests(TestCase):
    def test_home_without_param(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
        self.assertIn('titreh1', response.context)
        self.assertEqual(response.context['titreh1'], "Hello DJango !")
        self.assertContains(response, "Hello DJango !")

    def test_home_with_param(self):
        response = self.client.get(reverse('home_with_param', args=['Alice']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
        self.assertEqual(response.context['titreh1'], "Hello Alice !")
        self.assertContains(response, "Hello Alice !")

    def test_home_post_request(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
