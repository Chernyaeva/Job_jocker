from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='news_images', default="news_images/default_news_picture.jpg")
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

