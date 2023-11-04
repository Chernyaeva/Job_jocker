from django.shortcuts import render
from .models import News


def news(request):
    news = News.objects.all()
    return render(request, 'news.html', {'news':news})
