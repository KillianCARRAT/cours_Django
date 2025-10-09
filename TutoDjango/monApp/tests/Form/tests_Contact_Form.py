from django.test import TestCase
from monApp.forms import ContactUsForm
from django.urls import reverse

class ContactUsFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            'name': "UserTest",
            'email': "user.test@test.com",
            'message': "This is a test message."
        }

    def test_form_valid_data(self):
        form = ContactUsForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_data_too_long(self):
        self.form_data['message'] = 'A' * 1001
        form = ContactUsForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
        self.assertEqual(form.errors['message'], ['Assurez-vous que cette valeur comporte au plus 1000 caractères (actuellement 1001).'])
    
    def test_form_valid_data_missed(self):
        self.form_data['email'] = ''
        form = ContactUsForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = ContactUsForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('contact'), self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('email-sent'))
    