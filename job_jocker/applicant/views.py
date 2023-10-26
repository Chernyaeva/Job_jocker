from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from user.models import User
from django.shortcuts import render, redirect
from .models import Resume, Applicant, FavoriteVacancies
from employer.models import Vacancy, Application


def applicant_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    applicant = Applicant.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']
        address = request.POST['address']

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.user.phone = phone
        applicant.user.gender = gender
        applicant.user.address = address
        applicant.save()
        applicant.user.save()

        try:
            image = request.FILES['image']
            applicant.user.image = image
            applicant.user.save()
        except:
            pass
        alert = True
        return render(request, "applicant_homepage.html", {'alert':alert})
    return render(request, "applicant_homepage.html", {'applicant':applicant})


def all_resumes(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    applicant = Applicant.objects.get(user=request.user)
    resumes = Resume.objects.filter(applicant=applicant)
    return render(request, "all_resumes.html", {'resumes':resumes})

def resume(request, myid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    resume = Resume.objects.get(id=myid)
    applicant = Applicant.objects.get(user=request.user)
    return render(request, 'resume_detail.html', {'resume': resume, 'applicant': applicant})


def new_resume(request):
   if not request.user.is_authenticated:
        return redirect('/login/')
   if request.method == 'POST':
       profession = request.POST['profession']
       skills = request.POST['skills']
       education = request.POST['education']
       experience = request.POST['experience']
       salary = request.POST['salary']

       applicant = Applicant.objects.get(user=request.user)
       my_resume = Resume.objects.create(applicant=applicant,
                             name=request.user.first_name,
                             surname=request.user.last_name,
                             profession=profession,
                             skills=skills,
                             education=education,
                             experience=experience,
                             salary=salary)
       if request.POST['action'] == 'Опубликовать':
           my_resume.status = 'РАССМОТРЕНИЕ'
           my_resume.save()
           alert = True
           return render(request, "new_resume.html", {'alert_1': alert})
       alert = True
       return render(request, "new_resume.html", {'alert_2': alert})
   return render(request, "new_resume.html")


def delete_resume(request, myid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    Resume.objects.filter(id=myid).delete()
    return render(request, "resume_delete.html")


def edit_resume(request, myid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if not request.user.is_authenticated:
        return redirect('/applicant/login/')
    my_resume = Resume.objects.get(id=myid)
    if request.method == 'POST':
        profession = request.POST['profession']
        skills = request.POST['skills']
        education = request.POST['education']
        experience = request.POST['experience']
        salary = request.POST['salary']

        my_resume.profession = profession
        my_resume.skills = skills
        my_resume.education = education
        my_resume.experience = experience
        my_resume.salary = salary
        my_resume.status = 'ЧЕРНОВИК'
        my_resume.save()
        if request.POST['action'] == 'Опубликовать':
            my_resume.status = 'РАССМОТРЕНИЕ'
            my_resume.save()
            alert = True
            return render(request, 'resume_edit.html', {'alert_1': alert})
        alert = True
        return render(request, 'resume_edit.html', {'alert_2': alert})
    return render(request, 'resume_edit.html', {'resume': my_resume})




def all_vacancies_applicant(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    all_vacancies_applicant = Vacancy.objects.all()
    return render(request, "all_vacancies_applicant.html", {'all_vacancies_applicant': all_vacancies_applicant})



def applicant_vacancy_detail(request, pk):
    vacancyObj = Vacancy.objects.get(id=pk)
    applicant = Applicant.objects.get(user=request.user)
    favorite_vacancies = FavoriteVacancies.objects.filter(applicant=applicant)
    favorite_vacancies = Vacancy.objects.filter(id__in=favorite_vacancies)
    return render(request, 'applicant_vacancy_detail.html', {'vacancy': vacancyObj, 'favorite_vacancies':favorite_vacancies})


def choose_resume(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    applicant = Applicant.objects.get(user=request.user)
    resumes = Resume.objects.filter(applicant=applicant)
    return render(request, "choose_resume.html", {'resumes':resumes, 'vacancy':vacancy})


def application_sent(request, vacancy_id, resume_id):
    resume = Resume.objects.get(id=resume_id)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    user = User.objects.get(id = request.user.id)
    new_application = Application.objects.create(resume=resume,
                                                  vacancy=vacancy,
                                                  creator=user,
                                                  status='Отправлено работодателю')
    new_application.save()
    return render(request, "application_sent.html")

def applicant_applications(request):
    applicant = Applicant.objects.get(user=request.user)
    resumes = Resume.objects.filter(applicant = applicant)
    applications = Application.objects.filter(resume__in = resumes)
    return render(request, "applicant_applications.html", {'applications': applications})


def add_favorite_vacancy(request, vacancy_id):
    applicant = Applicant.objects.get(user=request.user)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    new_favorite_vacancy = FavoriteVacancies.objects.create(applicant=applicant, vacancy=vacancy)
    new_favorite_vacancy.save()
    return render(request, "add_favorite_vacancy.html")


def favorite_vacancies(request):
    applicant = Applicant.objects.get(user=request.user)
    favorite_vacancies = FavoriteVacancies.objects.filter(applicant=applicant)
    vacancies = Vacancy.objects.filter(id__in=favorite_vacancies)
    return render(request, "favorite_vacancies.html", {'vacancies':vacancies})