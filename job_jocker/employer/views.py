from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Card, Vacancy, FavoriteResumes, Application
from applicant.models import Resume, Applicant
from .utils import searchResumes, paginateResumes
from user.models import User, Chat



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


def employer_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    employer = Card.objects.get(user=request.user)
    if request.method == "POST":
        mail = request.POST['mail']
        name = request.POST['name']
        legal_form = request.POST['legal_form']
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
        employer.status = 'РАССМОТРЕНИЕ'

        employer.save()
        try:
            image = request.FILES['image']
            employer.logo = image
            employer.save()
        except:
            pass
        alert = True
        return render(request, "employer_homepage.html", {'alert': alert})
    return render(request, "employer_homepage.html", {'employer': employer})


def all_vacancy(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    vacancies = Vacancy.objects.all()
    return render(request, "all_vacancies.html", {'vacancies': vacancies})


def all_resumes_employer(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    resumes, search_query = searchResumes(request)
    custom_range, resumes = paginateResumes(request, resumes, 6)
    context = {'resumes': resumes,
            'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'all_resumes_employer.html', context)


def resume_employer(request, myid):
    if not request.user.is_authenticated:
        return redirect('/login/')
    resume = Resume.objects.get(id=myid)
    card = Card.objects.get(user=request.user)
    try:
        favorite_resume = FavoriteResumes.objects.filter(card=card)
    except:
        return render(request, 'resume_detail_employer.html',
                          {'resume': resume, 'card': card, 'alert': True})
    else:
        for i in favorite_resume:
            if i.resume == resume:
                return render(request, 'resume_detail_employer.html',
                              {'resume': resume, 'card': card, 'alert': False})
        return render(request, 'resume_detail_employer.html',
                              {'resume': resume, 'card': card, 'alert': True})


@login_required()
def add_favorite_resume(request, card_id, resume_id):
    card = Card.objects.get(id=card_id)
    resume = Resume.objects.get(id=resume_id)
    new_favorite_resume = FavoriteResumes.objects.create(card=card, resume=resume)
    new_favorite_resume.save()
    return render(request, "add_favorite_resume.html")


@login_required()
def favorite_resumes(request):
    card = Card.objects.get(user=request.user)
    favorite_resumes = FavoriteResumes.objects.filter(card=card)
    return render(request, "favorite_resumes.html", {'resumes': favorite_resumes})


@login_required()
def favorite_resume_delete(request, resume_id):
    card = Card.objects.get(user=request.user)
    resume = Resume.objects.get(id=resume_id)
    fav_resume = FavoriteResumes.objects.filter(card=card).filter(resume=resume)
    fav_resume.delete()
    return render(request, "favorite_resume_delete.html")


@login_required()
def employer_vacancies(request):
    card = Card.objects.get(user=request.user)
    vacancies = Vacancy.objects.filter(card_id=card)
    context = {'vacancies': vacancies}
    return render(request, 'employer_vacancies.html', context)


@login_required()
def vacancy_detail(request, pk):
    vacancyObj = Vacancy.objects.get(id=pk)
    return render(request, 'vacancy_detail.html', {'vacancy': vacancyObj})


@login_required()
def vacancy_new(request):
    if request.method == 'POST':
        profession = request.POST['profession']
        skills = request.POST['skills']
        education = request.POST['education']
        experience = request.POST['experience']
        salary = request.POST['salary']
        address = request.POST['address']
        description = request.POST['description']

        card = Card.objects.get(user=request.user)
        my_vacancy = Vacancy.objects.create(card_id=card,
                                            profession=profession,
                                            skills=skills,
                                            education=education,
                                            experience=experience,
                                            salary=salary,
                                            address=address,
                                            description=description
                                            )
        my_vacancy.save()
        alert = True
        return render(request, "vacancy_new.html", {'alert': alert})
    return render(request, "vacancy_new.html")


@login_required()
def vacancy_delete(request, myid):
    Vacancy.objects.filter(id=myid).delete()
    return render(request, "vacancy_delete.html")


def vacancy_edit(request, myid):
    if not request.user.is_authenticated:
        return redirect('/employer_login/')
    my_vacancy = Vacancy.objects.get(id=myid)
    if request.method == 'POST':
        profession = request.POST['profession']
        skills = request.POST['skills']
        education = request.POST['education']
        experience = request.POST['experience']
        salary = request.POST['salary']
        address = request.POST['address']
        description = request.POST['description']
        my_vacancy.profession = profession
        my_vacancy.skills = skills
        my_vacancy.education = education
        my_vacancy.experience = experience
        my_vacancy.salary = salary
        my_vacancy.address = address
        my_vacancy.description = description
        if request.POST['action'] == 'Опубликовать':
            my_vacancy.status = 'РАССМОТРЕНИЕ'
            my_vacancy.save()
            alert_1 = True
            return render(request, "vacancy_edit.html", {'alert_1': alert_1})
        elif request.POST['action'] == 'Сохранить':
            my_vacancy.status = 'ЧЕРНОВИК'
            my_vacancy.save()
            alert_2 = True
            return render(request, "vacancy_edit.html", {'alert_2': alert_2})
        elif request.POST['action'] == 'Комментарий':
            comment = my_vacancy.admin_comment
            date_comment = my_vacancy.date_comment
            return render(request, "vacancy_admin_comment.html",
                          {'comment': comment, 'date_comment': date_comment, 'id': my_vacancy.id})
    return render(request, 'vacancy_edit.html', {'vacancy': my_vacancy})


@login_required()
def choose_vacancy(request, resume_id):
    card = Card.objects.get(user=request.user)
    resume = Resume.objects.get(id=resume_id)
    vacancies = Vacancy.objects.filter(card_id=card).filter(status='ПУБЛИКАЦИЯ')
    return render(request, "choose_vacancy.html", {'resume': resume, 'vacancies': vacancies})


@login_required()
def offer_sent(request, vacancy_id, resume_id):
    resume = Resume.objects.get(id=resume_id)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    user = User.objects.get(id=request.user.id)
    try:
        applications = Application.objects.filter(resume=resume)
        for app in applications:
            if app.vacancy == vacancy:
                alert = True
                return render(request, "offer_sent.html", {'alert_repeat': alert})
    except:
        new_application = Application.objects.create(resume=resume,
                                                     vacancy=vacancy,
                                                     creator=user,
                                                     status='Отправлено')
        new_application.save()
        alert = True
        return render(request, "offer_sent.html", {'alert': alert})
    else:
        new_application = Application.objects.create(resume=resume,
                                                     vacancy=vacancy,
                                                     creator=user,
                                                     status='Отправлено')
        new_application.save()
        alert = True
        return render(request, "offer_sent.html", {'alert': alert})


@login_required()
def employer_applications(request):
    card = Card.objects.get(user=request.user)
    vacancies = Vacancy.objects.filter(card_id=card)
    applications = Application.objects.filter(vacancy__in=vacancies)
    return render(request, "employer_applications.html", {'applications': applications})


def employer_application_detail(request, application_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    application = Application.objects.get(id=application_id)
    applcant = Applicant.objects.get(id=application.resume.applicant.id)
    resume = Resume.objects.get(id=application.resume.id)
    return render(request, 'employer_application_detail.html',
                  {'application': application, 'applcant': applcant, 'resume': resume})


def employer_application_delete(request, application_id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    application = Application.objects.get(id=application_id)
    application.delete()
    return render(request, 'employer_application_delete.html')


@login_required()
def resume_answer(request, application_id, action):
    application = Application.objects.get(id=application_id)
    if action == 'ACCEPT':
        application.status = 'Принято'
        chat = Chat.objects.create(sender=application.resume.applicant.user, recipient=application.vacancy.card_id.user)
        application.chat = chat
    else:
        application.status = 'Отклонено'
    application.save()
    return render(request, "resume_answer.html", {'action': action})


@login_required()
def employer_admin_comment(request):
    card = Card.objects.get(user=request.user)
    comment = card.admin_comment
    date = card.date_comment
    context = {'comment': comment, 'date_comment': date}
    return render(request, 'employer_admin_comment.html', context)
