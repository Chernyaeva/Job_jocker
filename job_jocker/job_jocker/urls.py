"""job_jocker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views
from news import views as news_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('rules/', views.rules, name="rules"),
    path('login/', views.user_login, name="login"),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name="logout"),
    path('all_company/', views.index_all_company, name='index_all_company'),
    path('all_company/company_detail/<int:myid>/', views.index_company_detail, name='index_company_detail'),
    path('applicant/', include('applicant.urls')),
    path('employer/', include('employer.urls')),
    path('admin_site/', include('user.urls')),
    path('news/', include('news.urls')),
    path('chat/<int:chat_id>/', views.chat, name='chat'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

