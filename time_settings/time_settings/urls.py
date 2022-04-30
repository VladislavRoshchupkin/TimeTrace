"""time_settings URL Configuration

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
from app.views.views import *
from app.views.api_views import *
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
schema_view = get_swagger_view(
        title='TimeTrace API',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/project', ProjectList.as_view()),
    path('api/time', TimeList.as_view()),
    path('api/task', TaskList.as_view()),
    path('api/department', DepartmentList.as_view()),
    path('api/raiting', RaitingList.as_view()),
    path('api-swagger/', schema_view),
]
