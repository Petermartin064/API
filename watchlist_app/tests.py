from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')
        self.token = Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_streamplatform_create(self):
        data = {
            'name' : 'Netflix',
            'about' : 'Streaming platform',
            'website' : 'https://www.netflix.com'
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)