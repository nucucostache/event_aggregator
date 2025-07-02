from django.test import TestCase, Client
from django.urls import reverse

class APIClientViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_event_list_status_code(self):
        response = self.client.get(reverse('api_event_list'))
        self.assertEqual(response.status_code, 200)

    def test_api_event_list_template_used(self):
        response = self.client.get(reverse('api_event_list'))
        self.assertTemplateUsed(response, 'event_client/api_event_list.html')

