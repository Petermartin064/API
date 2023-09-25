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

class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')
        self.token = Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(Name='Netflix', About='streaming platform', Website='https://www.netflix.com')
        
        self.watchlist = models.WatchList.objects.create(Platform=self.stream, Title='FastX', Description='great movie', Active=True)
        
        self.watchlist2 = models.WatchList.objects.create(Platform=self.stream, Title='FastX', Description='great movie', Active=True)
        
        self.review = models.Review.objects.create(review_user = self.user, Rating = 5, Description = 'Good movie', Watchlist = self.watchlist2, Active = True)
        
    def test_review_create(self):
        data={
            'review_user' : self.user,
            'Rating' : 5,
            'Description' : 'Good movie',
            'Watchlist' : self.watchlist,
            'Active' : True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        data={
            'review_user' : self.user,
            'Rating' : 5,
            'Description' : 'Good movie',
            'Watchlist' : self.watchlist,
            'Active' : True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data={
            'review_user' : self.user,
            'Rating' : 4,
            'Description' : 'Great movie',
            'Watchlist' : self.watchlist,
            'Active' : True
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response= self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_ind(self):
        response= self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_del(self):
        data={
             'review_user' : self.user,
            'Rating' : 4,
            'Description' : 'Great movie',
            'Watchlist' : self.watchlist,
            'Active' : True
        }
        response =self.client.delete(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
