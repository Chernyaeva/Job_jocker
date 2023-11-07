from django.db.models import Q
from employer.models import Vacancy

def searchVacancies(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

 
    vacancies = Vacancy.objects.filter(status='ПУБЛИКАЦИЯ').distinct().filter(
        Q(profession__icontains=search_query) |
        Q(skills__icontains=search_query) |
        Q(description__icontains=search_query)
    )
    return vacancies, search_query