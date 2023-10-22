from django.urls import path
from . import views

urlpatterns = [
    path('', views.employer_homepage, name="employer_homepage"),
    path('signup/', views.employer_signup, name='employer_signup'),
    path('login/', views.employer_login, name='employer_login'),
    path('homepage/', views.employer_homepage, name='employer_homepage'),
    path('card-object/<str:pk>/', views.card, name="card"),
    path('vacancies/', views.vacancies, name="vacancies"),
    path('vacancy-object/<str:pk>/', views.vacancy, name="vacancy"),
    path('resumes/', views.all_resumes_employer, name="resumes"),
    path("resume/<int:myid>/", views.resume_employer, name="resume_employer"),
    path("add_favorite_resume/<int:card_id>/<int:resume_id>/", views.add_favorite_resume, name="add_favorite_resume"),
    path('favorite_resumes/', views.favorite_resumes, name="favorite_resumes"),
]