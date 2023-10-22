from django.urls import path
from . import views

urlpatterns = [
    path("homepage/", views.applicant_homepage, name="applicant_homepage"),
    path("all_resumes/", views.all_resumes, name="all_resumes"),
    path("new_resume/", views.new_resume, name="new_resume"),
    path("all_resumes/resume_detail/<int:myid>/", views.resume, name="resume"),
    path("all_resumes/resume_detail/<int:myid>/resume_edit/", views.edit_resume, name="edit_resume"),
    path("all_resumes/resume_detail/<int:myid>/resume_delete/", views.delete_resume, name="delete_resume"),
]
