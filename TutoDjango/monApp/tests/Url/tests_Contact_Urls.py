from django.test import TestCase
from django.urls import reverse, resolve
from monApp.views import ContactView

class ContactViewTests(TestCase):
    def test_login_url_resolves(self):
        url = reverse('contact')
        resolver = resolve(url)
        self.assertEqual(resolver.func, ContactView)
