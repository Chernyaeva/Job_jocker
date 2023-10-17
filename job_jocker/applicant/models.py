from django.db import models
from user.models import User


class Resume(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    skills = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=100)
    salary = models.IntegerField(default=0, null=True, blank=True)
    photo = models.ImageField(
        null=True, blank=True, upload_to='profile_images', default="profile_images/default.png")
    is_posted = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10, choices=[('Муж', 'Муж'), ('Жен', 'Жен')])
    role = models.CharField(max_length=10, default='applicant')

    def __str__(self):
        return self.user.first_name





