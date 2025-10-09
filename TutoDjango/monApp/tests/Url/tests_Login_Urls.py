from django.test import TestCase
from django.urls import reverse, resolve
from monApp.views import ConnectView, RegisterView, DisconnectView

class LoginViewTests(TestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ConnectView)

    def test_register_url_resolves(self):
        url = reverse('register')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, RegisterView)
    
    def test_logout_url_resolves(self):
        url = reverse('logout')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, DisconnectView)
