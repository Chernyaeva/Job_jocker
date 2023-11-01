from django.db import models
from user.models import User


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='applicant')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Resume(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    skills = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=256)
    experience = models.TextField(default='Без опыта', blank=False)
    salary = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=12, choices=[('ЧЕРНОВИК', 'ЧЕРНОВИК'), ('РАССМОТРЕНИЕ', 'РАССМОТРЕНИЕ'), ('ПУБЛИКАЦИЯ', 'ПУБЛИКАЦИЯ'),
                                                      ('ДОРАБОТКА', 'ДОРАБОТКА')], default='ЧЕРНОВИК')
    created = models.DateTimeField(auto_now_add=True)
    admin_comment = models.TextField(null=True, blank=True)
    date_comment = models.DateTimeField(null=True)


from employer.models import Vacancy 

class FavoriteVacancies(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vacancy.profession} в {self.vacancy.card_id.legal_form} {self.vacancy.card_id.name}"


