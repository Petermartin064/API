from django.db import models

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
    created = models.DateTimeField(auto_created=True)
    
    
    def __str__(self):
        return self.Title