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
        
        self.stream = models.StreamPlatform.objects.create(Name='Netflix', About='streaming platform', Website='https://www.netflix.com')
        
    def test_streamplatform_create(self):
        data = {
            'name' : 'Netflix',
            'about' : 'Streaming platform',
            'website' : 'https://www.netflix.com'
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response= self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_id(self):
        response =self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')
        self.token = Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(Name='Netflix', About='streaming platform', Website='https://www.netflix.com')
        
        self.watchlist = models.WatchList.objects.create(Platform=self.stream, Title='FastX', Description='great movie', Active=True)
        
    def test_watchlist_create(self):
        data ={
            'Platform' : self.stream,
            'Title' : 'Movie',
            'Description' : 'Great movie',
            'Active' : True
        }
        response =self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response= self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response= self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().Title, 'FastX')
        
    def test_watchlist_amd(self):
        data={
            'Platform' : self.stream,
            'Title' : 'Fast saga',
            'Description' : 'Good movie',
            'Active' : False
        }
        response =self.client.put(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_watchlist_del(self):
        data={
            'Platform' : self.stream,
            'Title' : 'Fast saga',
            'Description' : 'Good movie',
            'Active' : True
        }
        response =self.client.delete(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)