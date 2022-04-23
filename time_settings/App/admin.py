from django.contrib import admin
from .models import *

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'department_name', 'count_employee']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_key',
        'position_key',
        'department_key',
        'employee_surname',
        'employee_name',
        'employee_patronymic',
        'weekend_count',
    ]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project_name',
        'project_description',
        'start_date',
        'end_date',
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'task_key',
        # 'employee_key',
        'task_description',
    ]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'position_name',
    ]

@admin.register(Raiting)
class RaitingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'raiting_key',
        'total_count',
    ]

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'time_key',
        'date_work',
        'time_work',
    ]

