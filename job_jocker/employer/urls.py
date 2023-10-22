from django.urls import path
from . import views

urlpatterns = [
    path('', views.employer_homepage, name="employer_homepage"),
    path('signup/', views.employer_signup, name='employer_signup'),
    path('login/', views.employer_login, name='employer_login'),
    path('homepage/', views.employer_homepage, name='employer_homepage'),
    path('card-object/<str:pk>/', views.card, name="card"),
    path('employer_vacancies/', views.employer_vacancies, name="employer_vacancies"),
    path('vacancy_detail/<str:pk>/', views.vacancy_detail, name="vacancy_detail"),
    path('vacancy_edit/<str:myid>/', views.vacancy_edit, name="vacancy_edit"),
    path('vacancy_delete/<str:myid>/', views.vacancy_delete, name="vacancy_delete"),
    path('vacancy_new/', views.vacancy_new, name="vacancy_new"),
    path('choose_vacancy/<str:resume_id>/', views.choose_vacancy, name="choose_vacancy"),
    path('resumes/', views.all_resumes_employer, name="resumes"),
    path("resume/<int:myid>/", views.resume_employer, name="resume_employer"),
    path("add_favorite_resume/<int:card_id>/<int:resume_id>/", views.add_favorite_resume, name="add_favorite_resume"),
    path('favorite_resumes/', views.favorite_resumes, name="favorite_resumes"),
]