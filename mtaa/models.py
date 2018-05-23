from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hood(models.Model):
    hoodName = models.CharField(max_length=100)
    hoodLocation = models.CharField(max_length=50)
    occupantsCount = models.PositiveSmallIntegerField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.hoodName

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=500, blank=True)
    idNumber = models.PositiveSmallIntegerField()
    generalLocation = models.CharField(max_length=500, blank=True)
    email = models.EmailField(max_length=254)
    hood = models.ForeignKey(Hood)

class Business(models.Model):
    bizName = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    hood = models.ForeignKey(Hood)
    
    def __str__(self):
        return self.bizName

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    hood = models.ForeignKey(Hood)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
            
    class Meta:
        ordering = ['-postDate']
    
    def save_post(self):
        self.save()

class Social_Ammenities(models.Model):
    ammenityName = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    hood = models.ForeignKey(Hood)
    
    def __str__(self):
        return self.ammenityName

