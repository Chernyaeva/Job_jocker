from django.urls import path
from . import views

urlpatterns = [
    path("all_company/", views.all_company, name="all_company"),
    path("rules/", views.rules, name="rules"),
    path("company_detail/<int:myid>/", views.company_detail, name="company_detail"),
    path("company_comment/<int:myid>/", views.company_comment, name="company_comment"),
    path("all_vacancy/", views.all_vacancy, name="all_vacancy"),
    path("vacancy_detail/<int:myid>/", views.vacancy_detail, name="admin_vacancy_detail"),
    path("vacancy_comment/<int:myid>/", views.vacancy_comment, name="vacancy_comment"),
    path("all_resume/", views.all_resume, name="all_resume"),
    path("resume_detail/<int:myid>/", views.resume_detail, name="admin_resume_detail"),
    path("resume_comment/<int:myid>/", views.resume_comment, name="resume_comment"),
]