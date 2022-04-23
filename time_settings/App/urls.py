from django.urls import path
from .views.views import *
from .views.admin import employees, projects, tasks

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('profile/<int:id_task>/', get_tasks_for_employee, name='get_tasks_for_employee'),
    path('time_tracking/', time_tracking, name='time_tracking'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Путь для добавления сотрудника
    path('add_employee/',  employees.add_employee, name='add_employee'),

    # Путь для добавления проекта
    path('add_project/', projects.add_project, name='add_project'),
    path('add_task/', tasks.add_task, name='add_task'),
    path('raiting/', raiting, name='raiting'),
]
