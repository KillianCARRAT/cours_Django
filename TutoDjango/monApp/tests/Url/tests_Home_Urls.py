from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import HomeView

class HomeViewTests(TestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, HomeView)

    def test_home_with_param_url_resolves(self):
        url = reverse('home_with_param', args=['Alice'])
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, HomeView)
