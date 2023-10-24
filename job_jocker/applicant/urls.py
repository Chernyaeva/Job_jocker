from django.urls import path
from . import views

urlpatterns = [
    path("homepage/", views.applicant_homepage, name="applicant_homepage"),
    path("all_resumes/", views.all_resumes, name="all_resumes"),
    path("new_resume/", views.new_resume, name="new_resume"),
    path("all_resumes/resume_detail/<int:myid>/", views.resume, name="resume"),
    path("all_resumes/resume_detail/<int:myid>/resume_edit/", views.edit_resume, name="edit_resume"),
    path("all_resumes/resume_detail/<int:myid>/resume_delete/", views.delete_resume, name="delete_resume"),
    path('all_vacancies_applicant/', views.all_vacancies_applicant, name="all_vacancies_applicant"),
    path("vacancy/<str:pk>/", views.applicant_vacancy_detail, name="applicant_vacancy_detail"),
]
