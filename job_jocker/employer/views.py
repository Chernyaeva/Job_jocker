from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Card, Vacancy, FavoriteResumes
from applicant.models import Resume, Applicant
from django.contrib.auth.models import User

def cards(request):
    cards = Card.objects.all()
    context = {'cards': cards}
    return render(request, 'cards.html', context)

def card(request, pk):
    cardObj = Card.objects.get(id=pk)
    return render(request, 'one_card.html', {'card': cardObj})

def vacancies(request):
    vacancies = Vacancy.objects.all()
    context = {'vacancies': vacancies}
    return render(request, 'vacancies.html', context)

def vacancy(request, pk):
    vacancyObj = Vacancy.objects.get(id=pk)
    return render(request, 'one_vacancy.html', {'vacancy': vacancyObj})

def employer_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/employer/login/')
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


def employer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Card.objects.get(user=user)
                if user1.role == "employer":
                    login(request, user)
                    return redirect("/employer/homepage/")
                else:
                    thank = True
                    return render(request, "employer_login.html", {"thank": thank})
            else:
                thank = True
                return render(request, "employer_login.html", {"thank": thank})
    return render(request, "employer_login.html")


def all_vacancy(request):
    vacancies = Vacancy.objects.all()
    return render(request, "all_vacancies.html", {'vacancies': vacancies})


def employer_signup(request):
    if request.method == "POST":
        username = request.POST['email']
        first_name = 'noname'# request.POST['first_name']
        last_name = 'noname' # request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        name_company = request.POST['name_company']
        phone = request.POST['phone']
        legal_form = request.POST['legal_form']
        description = request.POST['description']
        address = request.POST['address']
        web_site = request.POST['web_site']
        inn = request.POST['inn']
        image = request.FILES['image']

        if password1 != password2:
            messages.error(request, "Введенные пароли не совпадают")
            return redirect('/employer/signup/')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        password=password1)
        employer = Card.objects.create(user=user, phone=phone, name=name_company,
                                       logo=image, mail=username, legal_form=legal_form,
                                       description=description, address=address,
                                       inn=inn, web_site=web_site, role='employer')
        user.save()
        employer.save()
        alert = True
        return render(request, "employer_signup.html", {'alert': alert})
    return render(request, "employer_signup.html")

def all_resumes_employer(request):
    resumes = Resume.objects.all()
    return render(request, "all_resumes_employer.html", {'resumes':resumes})

def resume_employer(request, myid):
    resume = Resume.objects.get(id=myid)
    applicant = Applicant.objects.get(user=resume.applicant.user)
    card = Card.objects.get(user=request.user)
    favorite_resumes = FavoriteResumes.objects.filter(card=card)
    favorite_resumes = Resume.objects.filter(id__in=favorite_resumes)
    return render(request, 'resume_detail_employer.html',{'resume':resume, 'applicant':applicant, 'card':card, 'favorite_resumes':favorite_resumes})


def add_favorite_resume(request, card_id, resume_id):
    card = Card.objects.get(id=card_id)
    resume = Resume.objects.get(id=resume_id)
    new_favorite_resume = FavoriteResumes.objects.create(card=card, resume=resume)
    new_favorite_resume.save()
    return render(request, "add_favorite_resume.html")


def favorite_resumes(request):
    card = Card.objects.get(user=request.user)
    favorite_resumes = FavoriteResumes.objects.filter(card=card)
    resumes = Resume.objects.filter(id__in=favorite_resumes)
    return render(request, "favorite_resumes.html", {'resumes':resumes})