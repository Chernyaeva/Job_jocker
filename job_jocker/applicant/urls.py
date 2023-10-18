from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("applicant_signup/", views.applicant_signup, name="applicant_signup"),
    path("applicant_login/", views.applicant_login, name="applicant_login"),
    path("applicant_homepage/", views.applicant_homepage, name="applicant_homepage"),
    path("applicant/all_resumes/", views.all_resumes, name="all_resumes"),
    path("applicant/new_resume/", views.new_resume, name="new_resume"),
    path("applicant/all_resumes/resume_detail/<int:myid>/", views.resume, name="resume"),
    path("applicant/all_resumes/resume_detail/<int:myid>/resume_edit/", views.edit_resume, name="edit_resume"),
    path("applicant/all_resumes/resume_detail/<int:myid>/resume_delete/", views.delete_resume, name="delete_resume"),
]
