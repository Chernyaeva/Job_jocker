from django.urls import path
from . import views

urlpatterns = [
    path('', views.applications, name="applications"),
    path('application-object/<str:pk>/', views.application, name="application"),
]