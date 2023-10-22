from django.db import models
#import user from user_app
from django.contrib.auth.models import User
from employer.models import Vacancy, Card
from applicant.models import Resume


# class Application(models.Model):
#     resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
#     vacancy_id = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
#     resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
#     creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     status = models.CharField(max_length=100)
#     created = models.DateTimeField(auto_now_add=True)
#     response = models.TextField(null=True, blank=True)

#     def __str__(self):
#         # return f"{Resume.objects.get(id=self.resume_id).profession}"
#         return f"{Resume.objects.get(id=self.resume_id.id).profession}"