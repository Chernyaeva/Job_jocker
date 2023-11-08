from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Q

from applicant.models import Applicant, Resume
from employer.models import Card, Vacancy
from user.models import User
from news.models import News
from .utils import searchCards, paginateCards


def index(request):
    resumes = Resume.objects.filter(status='ПУБЛИКАЦИЯ').order_by('-id')
    vacancies = Vacancy.objects.filter(status='ПУБЛИКАЦИЯ').order_by('-id')
    it_vacancies_count = vacancies.filter(Q(profession__icontains='Программист') |
                                          Q(profession__icontains='Разработчик') |
                                          Q(profession__icontains='IT') |
                                          Q(profession__icontains='SQL')).count()
    other_vacancies_count = vacancies.count() - it_vacancies_count

    context = {'resumes':resumes[:5],
               'vacancies':vacancies[:5], 
               'it_vacancies_count':it_vacancies_count, 
               'other_vacancies_count':other_vacancies_count,
               'vacancies_count': vacancies.count(),
               'resumes_count': resumes.count(),
               }

    return render(request, 'index.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)


            if user is not None:
                try:
                    my_user = User.objects.get(email=username)
                    if my_user.status == 'Админ':
                        login(request, user)
                        return redirect("/admin_site/all_company/")
                    elif my_user.status == 'Ищу работу':
                        login(request, user)
                        return redirect("/applicant/homepage")
                    elif my_user.status == 'Ищу сотрудника':
                        login(request, user)
                        return redirect("/employer/homepage")
                    else:
                        thank = True
                        return render(request, "login.html", {"thank": thank})
                except:
                    thank = True
                    return render(request, "login.html", {"thank": thank})
            else:
                thank = True
                return render(request, "login.html", {"thank": thank})
    return render(request, "login.html")


def user_signup(request):
    if request.method == "POST":
        try:
            username = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            phone = request.POST['phone']
            gender = request.POST['gender']
            image = request.FILES['image']
            status = request.POST['status']
            address = request.POST['address']

            if password1 != password2:
                messages.error(request, "Введенные пароли не совпадают")
                return redirect('/signup/')
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        password=password1, phone=phone, gender=gender, image=image, email=username,
                                        status=status, address=address)
            user.save()
            if user.status == 'Ищу работу':
                my_user = Applicant.objects.create(user=user, role='applicant')
                my_user.save()
                alert = True
                return render(request, "signup.html", {'alert_applicant': alert})
            else:
                my_user = Card.objects.create(user=user, role='employer')
                my_user.save()
                alert = True
                return render(request, "signup.html", {'alert_employer': alert})
        except:
            return render(request, "signup.html", {'alert_error': True})
    return render(request, "signup.html")


@login_required()
def all_company(request):
    companies = Card.objects.all().order_by('-status')
    custom_range, companies = paginateCards(request, companies, 6)
    context = {'companies': companies,
                'custom_range': custom_range}
    return render(request, "all_company.html", context)


@login_required()
def company_detail(request, myid):
    company = Card.objects.get(id=myid)
    if request.method == "POST":
        if request.POST['action'] == 'Публикация':
            company.status = 'ПУБЛИКАЦИЯ'
            company.save()
            return render(request, 'admin_navbar.html', {'alert': True})
        elif request.POST['action'] == 'Доработка':
            company.status = 'ДОРАБОТКА'
            company.save()
            return redirect(f'/admin_site/company_comment/{company.id}/')
        elif request.POST['action'] == 'Удалить':
            company.delete()
            return render(request, 'admin_navbar.html', {'alert_delete': True})
    return render(request, 'company_detail.html', {'company': company})


@login_required()
def company_comment(request, myid):
    company = Card.objects.get(id=myid)
    if request.method == "POST":
        comment = request.POST['comment']
        company.admin_comment = comment
        company.date_comment = datetime.now()
        company.save()
        return render(request, 'company_comment.html', {'alert': True})
    return render(request, 'company_comment.html')


def index_all_company_old(request):
    companies = Card.objects.all().filter(status='ПУБЛИКАЦИЯ')
    companies.order_by('created')
    return render(request, "index_all_company.html", {'companies': companies})



def index_all_company(request):
    cards, search_query = searchCards(request)
    custom_range, cards = paginateCards(request, cards, 6)
    context = {'companies': cards,
            'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'index_all_company.html', context)


def index_company_detail(request, myid):
    company = Card.objects.get(id=myid)
    return render(request, 'index_company_detail.html', {'company': company})


@login_required()
def all_vacancy(request):
    vacancies = Vacancy.objects.exclude(status='ЧЕРНОВИК').order_by('-status')
    return render(request, "all_vacancy.html", {'vacancies': vacancies})


@login_required()
def vacancy_detail(request, myid):
    vacancy = Vacancy.objects.get(id=myid)
    if request.method == "POST":
        if request.POST['action'] == 'Публикация':
            vacancy.status = 'ПУБЛИКАЦИЯ'
            vacancy.save()
            return render(request, 'admin_navbar.html', {'alert_vacancy': True})
        elif request.POST['action'] == 'Доработка':
            vacancy.status = 'ДОРАБОТКА'
            vacancy.save()
            return redirect(f'/admin_site/vacancy_comment/{vacancy.id}/')
        elif request.POST['action'] == 'Удалить':
            vacancy.delete()
            return render(request, 'admin_navbar.html', {'alert_vacancy_delete': True})
    return render(request, 'admin_vacancy_detail.html', {'vacancy': vacancy})


@login_required()
def vacancy_comment(request, myid):
    vacancy = Vacancy.objects.get(id=myid)
    if request.method == "POST":
        comment = request.POST['comment']
        vacancy.admin_comment = comment
        vacancy.date_comment = datetime.now()
        vacancy.save()
        return render(request, 'vacancy_comment.html', {'alert': True})
    return render(request, 'vacancy_comment.html')


@login_required()
def all_resume(request):
    resumes = Resume.objects.exclude(status='ЧЕРНОВИК').order_by('-status')
    return render(request, "all_resume.html", {'resumes': resumes})


@login_required()
def resume_detail(request, myid):
    resume = Resume.objects.get(id=myid)
    if request.method == "POST":
        if request.POST['action'] == 'Публикация':
            resume.status = 'ПУБЛИКАЦИЯ'
            resume.save()
            return render(request, 'admin_navbar.html', {'alert_resume': True})
        elif request.POST['action'] == 'Доработка':
            resume.status = 'ДОРАБОТКА'
            resume.save()
            return redirect(f'/admin_site/resume_comment/{resume.id}/')
        elif request.POST['action'] == 'Удалить':
            resume.delete()
            return render(request, 'admin_navbar.html', {'alert_resume_delete': True})
    return render(request, 'admin_resume_detail.html', {'resume': resume})


@login_required()
def resume_comment(request, myid):
    resume = Resume.objects.get(id=myid)
    if request.method == "POST":
        comment = request.POST['comment']
        resume.admin_comment = comment
        resume.date_comment = datetime.now()
        resume.save()
        return render(request, 'resume_comment.html', {'alert': True})
    return render(request, 'resume_comment.html')

