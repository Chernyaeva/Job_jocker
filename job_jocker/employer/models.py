from django.db import models

from user.models import User, Chat


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
    status = models.CharField(max_length=12, choices=[('ПУБЛИКАЦИЯ', 'ПУБЛИКАЦИЯ'),
                                                         ('РАССМОТРЕНИЕ', 'РАССМОТРЕНИЕ'),
                                                         ('ДОРАБОТКА', 'ДОРАБОТКА')], default='РАССМОТРЕНИЕ')
    logo = models.ImageField(upload_to='logo_images', default="logo_images/default_logo.jpg")
    is_posted = models.BooleanField(default=False, null=True)
    admin_comment = models.TextField(null=True, blank=True)
    date_comment = models.DateTimeField(null=True)
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
    status = models.CharField(max_length=12, choices=[('ПУБЛИКАЦИЯ', 'ПУБЛИКАЦИЯ'),
                                                         ('ЧЕРНОВИК', 'ЧЕРНОВИК'),
                                                         ('РАССМОТРЕНИЕ', 'РАССМОТРЕНИЕ'),
                                                         ('ДОРАБОТКА', 'ДОРАБОТКА')], default='РАССМОТРЕНИЕ')
    admin_comment = models.TextField()
    date_comment = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profession}"


from applicant.models import Resume

class FavoriteResumes(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume.surname}, {self.resume.profession}"
    

class Application(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=300)
    response = models.TextField(null=True, blank=True)
    chat = models.ForeignKey(Chat, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.vacancy.card_id.name}, {self.resume.surname}, {self.resume.profession}"
