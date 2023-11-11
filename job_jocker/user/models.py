from django.contrib.auth.models import User
from django.db import models


class User(User):
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to="", null=True)
    gender = models.CharField(max_length=10, choices=[('Муж', 'Муж'), ('Жен', 'Жен')])
    address = models.CharField(max_length=300)
    status = models.CharField(max_length=15, null=True)


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    created = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    to_send = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
