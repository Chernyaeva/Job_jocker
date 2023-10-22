from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect

from applicant.models import Applicant
from employer.models import Card
from user.models import User


def index(request):
    return render(request, "index.html")


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
                my_user = User.objects.get(email=username)
                if my_user.status == 'Ищу работу':
                    login(request, user)
                    return redirect("/applicant/homepage")

                elif my_user.status == 'Ищу сотрудника':
                    login(request, user)
                    return redirect("/employer/homepage")
                else:
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



