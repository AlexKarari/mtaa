from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Hood(models.Model):
    hoodName = models.CharField(max_length=100)
    hoodLocation = models.CharField(max_length=50, null=True)
    occupantsCount = models.PositiveSmallIntegerField(null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.hoodName

    def save_hood(self):
        self.save()

    def delete_hood(self):
        self.delete()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    idNumber = models.CharField(max_length=500, null=True, unique=True)
    name = models.CharField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profilepic/')
    generalLocation = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254)
    hood = models.ForeignKey(Hood, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Business(models.Model):
    business_name = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description_of_biz = models.TextField(null=True)
    location = models.CharField(max_length=1000, null=True)
    email = models.EmailField(max_length=254)
    
    hood = models.ForeignKey(Hood, null=True)

    @classmethod
    def search_by_business_name(cls, search_term):
        business = cls.objects.filter(business_name__icontains=search_term)
        return business
    
    def __str__(self):
        return self.business_name

    def save_business(self):
        self.save()

    def delete_business(self):
        self.delete()

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    hood = models.ForeignKey(Hood, null=True)
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
    hood = models.ForeignKey(Hood, null=True)
    
    def __str__(self):
        return self.ammenityName


class Join(models.Model):
	'''
	Model that keeps track of users and the neighbourhoods they're in
	'''
	user_id = models.ForeignKey(User)
	hood_id = models.ForeignKey(Hood)

	def __str__(self):
		return self.user_id
