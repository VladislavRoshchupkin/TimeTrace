from django.urls import path
from .views.views import *
from .views.admin import employees, projects, tasks

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('profile/task/<int:id_project>/', get_tasks_for_employee, name='get_tasks_for_employee'),
    path('time_tracking/<int:id>', time_tracking, name='time_tracking'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Путь для добавления сотрудника
    path('add_employee/',  employees.add_employee, name='add_employee'),

    # Путь для добавления проекта
    path('add_project/', projects.add_project, name='add_project'),
    path('add_task/', tasks.add_task, name='add_task'),
    path('raiting/', raiting, name='raiting'),

    # Изменение профиля
    path('profile/edit/<int:id>', edit_user, name='edit_user'),

    # Изменение проекта
    path('profile/<int:id>/edit', projects.edit_project, name='edit_project'),
    # Удаления проекта
    path('profile/<int:id>/delete_project', projects.delete_project, name='delete_project'),

    # Изменение задачи
    path('task/<int:id>/edit', tasks.edit_task, name='edit_task'),
    # Удаления задачи
    path('task/<int:id>/delete_task', tasks.delete_task, name='delete_task'),
]
