from django.urls import path
from .views.views import *
from .views.admin import add_employees, add_projects

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('profile/<int:id_task>/', get_tasks_for_employee, name='get_tasks_for_employee'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Путь для добавления сотрудника
    path('add_employee/',  add_employees.add_employee, name='add_employee'),

    # Путь для добавления проекта
    path('add_project/', add_projects.add_project, name='add_project'),


]
