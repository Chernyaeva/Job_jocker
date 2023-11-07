from django.db.models import Q
from applicant.models import Resume

def searchResumes(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

 
    resumes = Resume.objects.filter(status='ПУБЛИКАЦИЯ').distinct().filter(
        Q(profession__icontains=search_query) |
        Q(skills__icontains=search_query) |
        Q(education__icontains=search_query)
    )
    return resumes, search_query