from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        

    # Connect view tests
    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_login.html')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
        self.assertContains(response, "You are connected")
        self.assertIn('param', response.context)
        self.assertEqual(response.context['param'], 'admin')

    def test_login_failure_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'badpass',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_register.html')

    def test_login_failure_no_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'bob',
            'password': 'admin',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_register.html')

    # Register view tests
    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_register.html')

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'mail': 'admin@example.com',
            'password': 'testuser',
        })

        self.assertTrue(User.objects.filter(username='testuser').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_login.html')

    def test_register_failure_no_data(self):
        response = self.client.post(reverse('register'), {})
        self.assertEqual(User.objects.count(), 1) # admin is create

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_register.html')

    
    # Disconnect view tests
    def test_logout_view(self):
        self.client.login(username='admin', password='admin')
        response_before = self.client.get('/')
        self.assertTrue('_auth_user_id' in self.client.session)

        response = self.client.get(reverse('logout'))

        self.assertFalse('_auth_user_id' in self.client.session)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_logout.html')