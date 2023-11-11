from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core import paginator

from user.models import User, Chat
from django.shortcuts import render, redirect
from .models import Resume, Applicant, FavoriteVacancies
from employer.models import Vacancy, Application
from .utils import searchVacancies, paginateVacancies


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
        elif request.POST['action'] == 'Комментарий':
             comment = my_resume.admin_comment
             date_comment = my_resume.date_comment
             return render(request, "resume_admin_comment.html", {'comment': comment, 'date_comment': date_comment, 'id': my_resume.id})
        alert = True
        return render(request, 'resume_edit.html', {'alert_2': alert})
    return render(request, 'resume_edit.html', {'resume': my_resume})


def all_vacancies_applicant_old(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    vacancies = []
    all_public_vacancy = Vacancy.objects.filter(status='ПУБЛИКАЦИЯ')
    for vacancy in all_public_vacancy:
        if vacancy.card_id.status == 'ПУБЛИКАЦИЯ':
            vacancies.append(vacancy)
    return render(request, "all_vacancies_applicant.html", {'vacancies': vacancies})


def all_vacancies_applicant(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    vacancies, search_query = searchVacancies(request)
    custom_range, vacancies = paginateVacancies(request, vacancies, 6)
    context = {'vacancies': vacancies,
            'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'all_vacancies_applicant.html', context)


@login_required()
def favorite_vacancy_delete(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    applicant = Applicant.objects.get(user=request.user)
    favorite_vacancy = FavoriteVacancies.objects.filter(vacancy=vacancy).filter(applicant=applicant)
    favorite_vacancy.delete()
    return render(request, 'favorite_vacancy_delete.html')


@login_required()
def applicant_vacancy_detail(request, pk):
    vacancyObj = Vacancy.objects.get(id=pk)
    applicant = Applicant.objects.get(user=request.user)
    try:
        favorite_vacancy = FavoriteVacancies.objects.filter(applicant=applicant)
    except:
        return render(request, 'applicant_vacancy_detail.html',
                          {'vacancy': vacancyObj, 'alert': True})
    else:
        for i in favorite_vacancy:
            if i.vacancy == vacancyObj:
                return render(request, 'applicant_vacancy_detail.html',
                              {'vacancy': vacancyObj, 'alert': False})
        return render(request, 'applicant_vacancy_detail.html', {'vacancy': vacancyObj, 'alert': True})


@login_required()
def choose_resume(request, vacancy_id):
    applicant = Applicant.objects.get(user=request.user)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    resumes = Resume.objects.filter(applicant=applicant).filter(status='ПУБЛИКАЦИЯ')
    if len(Resume.objects.filter(applicant=applicant)) == 0:
        return render(request, "choose_resume.html", {'alert': True})
    elif len(resumes) == 0:
        return render(request, "choose_resume.html", {'alert_1': True})
    return render(request, "choose_resume.html", {'resumes': resumes, 'vacancy': vacancy})



@login_required()
def application_sent(request, vacancy_id, resume_id):
    resume = Resume.objects.get(id=resume_id)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    user = User.objects.get(id=request.user.id)
    try:
        application = Application.objects.filter(vacancy=vacancy)
        for app in application:
            if app.resume == resume:
                return render(request, "application_sent.html", {'alert_repeat': True})
    except:
        new_application = Application.objects.create(resume=resume,
                                                  vacancy=vacancy,
                                                  creator=user,
                                                  status='Отправлено')
        new_application.save()
        alert = True
        return render(request, "application_sent.html", {'alert': alert})
    else:
        new_application = Application.objects.create(resume=resume,
                                                     vacancy=vacancy,
                                                     creator=user,
                                                     status='Отправлено')
        new_application.save()
        alert = True
        return render(request, "application_sent.html", {'alert': alert})


@login_required()
def applicant_applications(request):
    applicant = Applicant.objects.get(user=request.user)
    resumes = Resume.objects.filter(applicant = applicant)
    applications = Application.objects.filter(resume__in = resumes)
    return render(request, "applicant_applications.html", {'applications': applications})


def applicant_application_detail(request, application_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    application = Application.objects.get(id=application_id)
    vacancy = Vacancy.objects.get(id=application.vacancy.id)
    resume = Resume.objects.get(id=application.resume.id)
    return render(request, 'applicant_application_detail.html',{'application':application,'vacancy':vacancy,'resume':resume})


def applicant_application_delete(request, application_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    application = Application.objects.get(id=application_id)
    application.delete()
    return render(request, 'applicant_application_delete.html', {'alert': True})


@login_required()
def vacancy_answer(request, application_id, action):
    application = Application.objects.get(id=application_id)
    if action == 'ACCEPT':
        application.status = 'Принято'
        chat = Chat.objects.create(sender=application.resume.applicant.user, recipient=application.vacancy.card_id.user)
        application.chat = chat

    else:
        application.status = 'Отклонено'    
    application.save()
    return render(request, "vacancy_answer.html", {'action': action})


@login_required()
def add_favorite_vacancy(request, vacancy_id):
    applicant = Applicant.objects.get(user=request.user)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    new_favorite_vacancy = FavoriteVacancies.objects.create(applicant=applicant, vacancy=vacancy)
    new_favorite_vacancy.save()
    return render(request, "add_favorite_vacancy.html")


@login_required()
def favorite_vacancies(request):
    applicant = Applicant.objects.get(user=request.user)
    vacancies = FavoriteVacancies.objects.filter(applicant=applicant)
    return render(request, "favorite_vacancies.html", {'vacancies':vacancies})