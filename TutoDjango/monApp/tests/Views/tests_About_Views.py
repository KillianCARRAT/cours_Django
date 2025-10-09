from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import AboutView

from django.test import TestCase
from django.urls import reverse

class AboutViewTests(TestCase):
    def test_about(self):
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
        self.assertIn('titreh1', response.context)
        self.assertEqual(response.context['titreh1'], "About us...")
        self.assertContains(response, "About us...")

    def test_home_post_request(self):
        response = self.client.post(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
