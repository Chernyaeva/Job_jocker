from django.db import models
from user.models import User


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    legal_form = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=300)
    inn = models.IntegerField(default=0)
    phone = models.CharField(max_length=20)
    web_site = models.CharField(max_length=100)

    logo = models.ImageField(upload_to='profile_images', default="logo_images/default_logo.jpg")
    is_posted = models.BooleanField(default=False, null=True)
    admin_comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, default='employer')

    def __str__(self):
        return f"{self.user}"
    

class Vacancy(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    experience = models.TextField()
    skills = models.TextField()
    education = models.CharField(max_length=100)
    salary = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=300)
    is_posted = models.BooleanField(default=False)
    admin_comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.profession}"

