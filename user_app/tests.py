from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            'username' : 'testcase',
            'email' : 'test@gmail.com',
            'password' : 'password123',
            'password2' : 'password123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)