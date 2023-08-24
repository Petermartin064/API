from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    Name = models.CharField(max_length= 50)
    About = models.CharField(max_length= 150)
    Website = models.URLField(max_length=100)

    def __str__(self):
        return self.Name
class WatchList(models.Model):
    Title = models.CharField(max_length= 50)
    Description = models.CharField(max_length= 200)
    active = models.BooleanField(default= True)
    Platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="WatchList")
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Title
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    Description = models.CharField(max_length=200, null=True)
    Watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    Active = models.BooleanField(default=True)
    Created = models.DateTimeField(auto_created=True)
    Update= models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return str(self.Rating) + " | " + self.Watchlist.Title
    