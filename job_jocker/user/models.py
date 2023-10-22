from django.contrib.auth.models import User
from django.db import models


class User(User):
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to="", null=True)
    gender = models.CharField(max_length=10, choices=[('Муж', 'Муж'), ('Жен', 'Жен')])
    address = models.CharField(max_length=300)
    status = models.CharField(max_length=15, null=True)

