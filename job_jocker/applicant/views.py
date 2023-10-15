from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Resume, Applicant


def index(request):
    return render(request, "index.html")


def resumes(request):
    resumes = Resume.objects.all()
    context = {'resumes': resumes}
    return render(request, 'resumes.html', context)

def resume(request, pk):
    resumeObj = Resume.objects.get(id=pk)
    return render(request, 'one_resume.html', {'resume': resumeObj})


def applicant_signup(request):
    if request.method == "POST":
        username = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']

        if password1 != password2:
            messages.error(request, "Введенные пароли не совпадают")
            return redirect('/applicant_signup')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        password=password1)
        applicants = Applicant.objects.create(user=user, phone=phone, gender=gender, image=image, email=username, role='applicant')
        user.save()
        applicants.save()
        alert = True
        return render(request, "applicant_signup.html", {'alert': alert})
    return render(request, "applicant_signup.html")


def applicant_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user1.role == "applicant":
                    login(request, user)
                    return redirect("/applicant_homepage")
            else:
                thank = True
                return render(request, "applicant_login.html", {"thank": thank})
    return render(request, "applicant_login.html")


def Logout(request):
    logout(request)
    return redirect('/')


def applicant_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/applicant_login/')
    applicant = Applicant.objects.get(user=request.user)
    if request.method=="POST":
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()

        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()
        except:
            pass
        alert = True
        return render(request, "applicant_homepage.html", {'alert':alert})
    return render(request, "applicant_homepage.html", {'applicant':applicant})

