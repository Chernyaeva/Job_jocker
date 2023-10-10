from django.urls import path
from . import views

urlpatterns = [
    path('', views.resumes, name="resumes"),
    path('resume-object/<str:pk>/', views.resume, name="resume"),
]