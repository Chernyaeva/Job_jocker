from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("applicant_signup/", views.applicant_signup, name="applicant_signup"),
    path("applicant_login/", views.applicant_login, name="applicant_login"),
    path("applicant_homepage/", views.applicant_homepage, name="applicant_homepage"),
    path('resume-object/<str:pk>/', views.resume, name="resume"),
]