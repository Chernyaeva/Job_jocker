from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Card, Vacancy
from applicant.models import Resume, Applicant
from django.contrib.auth.models import User


def cards(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    cards = Card.objects.all()
    context = {'cards': cards}
    return render(request, 'cards.html', context)

def card(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
    cardObj = Card.objects.get(id=pk)
    return render(request, 'one_card.html', {'card': cardObj})

def vacancies(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    vacancies = Vacancy.objects.all()
    context = {'vacancies': vacancies}
    return render(request, 'vacancies.html', context)

def vacancy(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
    vacancyObj = Vacancy.objects.get(id=pk)
    return render(request, 'one_vacancy.html', {'vacancy': vacancyObj})

def employer_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    employer = Card.objects.get(user=request.user)
    if request.method=="POST":
        mail = request.POST['mail']
        name=request.POST['name']
        legal_form=request.POST['legal_form']
        phone = request.POST['phone']
        web_site = request.POST['web_site']
        inn = request.POST['inn']
        description = request.POST["description"]
        address = request.POST["address"]

        employer.mail = mail
        employer.name = name
        employer.legal_form = legal_form
        employer.phone = phone
        employer.web_site = web_site
        employer.inn = inn
        employer.description = description
        employer.address = address

        employer.save()
        try:
            image = request.FILES['image']
            employer.logo = image
            employer.save()
        except:
            pass
        alert = True
        return render(request, "employer_homepage.html", {'alert':alert})
    return render(request, "employer_homepage.html", {'employer':employer})


def all_vacancy(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    vacancies = Vacancy.objects.all()
    return render(request, "all_vacancies.html", {'vacancies': vacancies})


def all_resumes_employer(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    resumes = Resume.objects.all()
    return render(request, "all_resumes_employer.html", {'resumes':resumes})


def resume_employer(request, myid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    resume = Resume.objects.get(id=myid)
    applicant = Applicant.objects.get(user=resume.applicant.user)
    return render(request, 'resume_detail_employer.html',{'resume':resume, 'applicant':applicant})