from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.
class TestGetToken(APITestCase):
    def test_create_account(self):
        data = {'username': 'surfer123', 'password': 'wAves13!'}
        resp = self.client.post('/register', data, format = 'json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
