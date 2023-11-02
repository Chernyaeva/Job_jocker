from django.shortcuts import render
from .models import News

def news_detail(request, news_item_id):
    news_item = News.objects.get(id=news_item_id)
    return render(request, 'news_detail.html', {'news_item':news_item})
