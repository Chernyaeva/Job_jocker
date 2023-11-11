from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_index, name="admin_site"),
    path("all_company/", views.all_company, name="all_company"),
    path("company_detail/<int:myid>/", views.company_detail, name="company_detail"),
    path("company_comment/<int:myid>/", views.company_comment, name="company_comment"),
    path("all_vacancy/", views.all_vacancy, name="all_vacancy"),
    path("rules/", views.rules, name="rules"),
    path("vacancy_detail/<int:myid>/", views.vacancy_detail, name="admin_vacancy_detail"),
    path("vacancy_comment/<int:myid>/", views.vacancy_comment, name="vacancy_comment"),
    path("all_resume/", views.all_resume, name="all_resume"),
    path("resume_detail/<int:myid>/", views.resume_detail, name="admin_resume_detail"),
    path("resume_comment/<int:myid>/", views.resume_comment, name="resume_comment"),
    path("news/", views.admin_news, name="admin_news"),
    path("new_news/", views.admin_new_news, name="admin_new_news"),
    path("news/<int:id>/", views.admin_news_detail, name="admin_news_detail"),
    path('logout/', views.user_logout, name="logout"),
]