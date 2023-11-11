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
    path('choose_resume/<int:vacancy_id>/', views.choose_resume, name="choose_resume"),
    path("add_favorite_vacancy/<int:vacancy_id>/", views.add_favorite_vacancy, name="add_favorite_vacancy"),
    path('favorite_vacancies/', views.favorite_vacancies, name="favorite_vacancies"),
    path('favorite_vacancy_delete/<int:vacancy_id>/', views.favorite_vacancy_delete, name="favorite_vacancy_delete"),
    path("application_sent/<int:vacancy_id>/<int:resume_id>/", views.application_sent, name="application_sent"),
    path('applicant_applications/', views.applicant_applications, name="applicant_applications"),
    path('applicant_application_detail/<int:application_id>/', views.applicant_application_detail, name="applicant_application_detail"),
    path('applicant_application_delete/<int:application_id>/', views.applicant_application_delete, name="applicant_application_delete"),
    path('vacancy_answer/<int:application_id>/<str:action>/', views.vacancy_answer, name="vacancy_answer"),
]
