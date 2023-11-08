from django.db.models import Q
from employer.models import Card
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchCards(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

 
    cards = Card.objects.filter(status='ПУБЛИКАЦИЯ').distinct().filter(
        Q(name__icontains=search_query) |
        Q(legal_form__icontains=search_query) |
        Q(description__icontains=search_query) | 
        Q(address__icontains=search_query) 
    )
    return cards, search_query


def paginateCards(request, cards, results):

    page = request.GET.get('page')
    paginator = Paginator(cards, results)

    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        cards = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        cards = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, cards