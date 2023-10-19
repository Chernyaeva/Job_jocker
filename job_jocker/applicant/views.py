from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Resume, Applicant


def index(request):
    return render(request, "index.html")


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
    if request.method == "POST":
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


def all_resumes(request):
    applicant = Applicant.objects.get(user=request.user)
    resumes = Resume.objects.filter(applicant=applicant)
    return render(request, "all_resumes.html", {'resumes':resumes})

def resume(request, myid):
    resume = Resume.objects.get(id=myid)
    applicant = Applicant.objects.get(user=request.user)
    return render(request, 'resume_detail.html',{'resume':resume, 'applicant':applicant})


def new_resume(request):
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
                             salary=salary,)
       my_resume.save()
       try:
           image = request.FILES['image']
           my_resume.photo = image
           my_resume.save()
       except:
           pass
       alert = True
       return render(request, "new_resume.html", {'alert': alert})
   return render(request, "new_resume.html")


def delete_resume(request, myid):
    Resume.objects.filter(id=myid).delete()
    return render(request, "resume_delete.html")


def edit_resume(request, myid):
    if not request.user.is_authenticated:
        return redirect('/applicant_login/')
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
        my_resume.status = 'РАССМОТРЕНИЕ'
        my_resume.save()
        try:
            image = request.FILES['image']
            my_resume.photo = image
            my_resume.save()
        except:
            pass
        alert = True
        return render(request, 'resume_edit.html', {'alert': alert})
    return render(request, 'resume_edit.html', {'resume': my_resume})







