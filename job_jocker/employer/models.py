from django.db import models
#import user from user_app 
import uuid

class Card(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    legal_form = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=300)
    inn = models.IntegerField(default=0, null=True, blank=True)
    web_site = models.CharField(max_length=100)

    logo = models.ImageField(
        null=True, blank=True, upload_to='profile_images', default="logo_images/default_logo.jpg")
    is_posted = models.BooleanField(default=False, null=True)
    admin_comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.name}"
    

class Vacancy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=100)
    salary = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=300)
    is_posted = models.BooleanField(default=False, null=True)
    admin_comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.profession}"

