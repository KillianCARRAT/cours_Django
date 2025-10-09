from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import AboutView

class AboutViewTests(TestCase):
    def test_about_url_resolves(self):
        url = reverse('about')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, AboutView)

