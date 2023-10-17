from django.shortcuts import render

from .models import Application
from employer.models import Vacancy, Card
from applicant.models import Resume
from user.models import User

def applications(request):
    applications = Application.objects.all()
    context = {'applications': applications}
    return render(request, 'applications.html', context)

def application(request, pk):
    applicationObj = Application.objects.get(id=pk)
    application_resume = Resume.objects.get(id=applicationObj.resume_id.id)
    application_vacancy = Vacancy.objects.get(id=applicationObj.vacancy_id.id)
    application_creator = User.objects.get(id=applicationObj.creator_id.id)
    application_card = Card.objects.get(id=application_creator.id)
    context = {'application': applicationObj,
                 'application_resume': application_resume,
                 'application_vacancy': application_vacancy,
                 'aplication_creator': application_creator,
                 'application_card': application_card
                 }
    return render(request, 'one_application.html', context)
