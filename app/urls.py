from django.urls import path
from .views.views import *
from .views.admin import employees, projects, tasks
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),

    # часы сторудников
    path('profile/time_work/<int:id>', get_time_all, name='get_time_all'),
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
    path('raiting_for_admin/', raiting_demo, name='raiting_demo'),
    path('raiting_page/<int:id>/', raiting_page, name='raiting_page'),
    path('show_employee_for_dep/<int:id>/', show_employee_for_dep, name='show_employee_for_dep'),
    
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

    # Добавление выходного
    path('add_weekend/<int:id>/', add_weekend, name='add_weekend'),
    
    path('change_time_work/<int:id>/', change_time_work, name='change_time_work'),

    path('unread_notifications/', unread_notifications, name='unread_notifications'),

    path('profile_page/<int:id>', profile_page, name='profile_page'),

    path('search/', search_querys, name='search_url')

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
