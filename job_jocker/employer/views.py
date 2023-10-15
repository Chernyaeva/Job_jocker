from django.shortcuts import render
from .models import Card, Vacancy

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