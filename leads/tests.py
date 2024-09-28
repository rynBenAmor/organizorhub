from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class LandingPageTest(TestCase):
    def test_status_quo(self):
        response = self.client.get(reverse('leads:landing'))
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, "leads/landing.html")

    