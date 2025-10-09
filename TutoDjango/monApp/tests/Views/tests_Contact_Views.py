from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from monApp.forms import ContactUsForm

class ContactView(TestCase):
    def setUp(self):
        self.form_data = {
            'name': "UserTest",
            'email': "user.test@test.com",
            'message': "This is a test message."
        }

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'), data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')

        self.assertIsInstance(response.context['form'], ContactUsForm)
        self.assertIn('titreh1', response.context)
        self.assertEqual(response.context['titreh1'], 'Contact us !')

    def test_post_valid_data_sends_email_and_redirects(self):
        response = self.client.post(reverse('contact'), data=self.form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('email-sent'))

        # Test sur l'email trouvé sur chatgpt => django.core
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn('UserTest', sent_email.subject)
        self.assertIn('This is a test message.', sent_email.body)
        self.assertEqual(sent_email.from_email, "user.test@test.com")
        self.assertEqual(sent_email.to, ['admin@monprojet.com'])

    def test_post_invalid_data_rerenders_form(self):
        self.form_data['email'] = ''
        response = self.client.post(reverse('contact'), data=self.form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
        self.assertFalse(response.context['form'].is_valid())

        self.assertIn('email', response.context['form'].errors)
        self.assertEqual(len(mail.outbox), 0)