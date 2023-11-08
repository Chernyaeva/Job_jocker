from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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


def paginateResumes(request, resumes, results):

    page = request.GET.get('page')
    paginator = Paginator(resumes, results)

    try:
        resumes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        resumes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        resumes = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, resumes