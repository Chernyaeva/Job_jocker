from django.shortcuts import render
from .models import Resume

def resumes(request):
    resumes = Resume.objects.all()
    context = {'resumes': resumes}
    return render(request, 'resumes.html', context)

def resume(request, pk):
    resumeObj = Resume.objects.get(id=pk)
    return render(request, 'one_resume.html', {'resume': resumeObj})