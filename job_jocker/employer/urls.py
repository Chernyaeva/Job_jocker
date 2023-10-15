from django.urls import path
from . import views

urlpatterns = [
    path('', views.cards, name="cards"),
    path('card-object/<str:pk>/', views.card, name="card"),
    path('vacancies/', views.vacancies, name="vacancies"),
    path('vacancy-object/<str:pk>/', views.vacancy, name="vacancy"),
]