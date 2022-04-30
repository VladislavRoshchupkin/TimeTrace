from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'task_key',
            'employee_key',
            'task_name',
            'task_description',
            'start_date_task',
            'end_date_task',
            'completed',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 
            'project_user_key',
            'manager_key',
            'project_name',
            'project_description',
            'start_date',
            'end_date',
        ]

class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = [
            'id',
            'time_key',
            'task_key',
            'description',
            'date_work',
            'time_work',
        ]

    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'department_name',
            'count_employee',
        ]

class RaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raiting
        fields = [
            'id',
            'raiting_key',
            'total_count',
        ]


    
