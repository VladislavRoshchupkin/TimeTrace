from django import forms
from app.models import *

class EmployeeAddedForms(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = [
            # 'user_key',
            'department_key',
            'position_key',
            'employee_surname',
            'employee_name',
            'employee_patronymic',
        ]


class ProjectAddedForms(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_user_key',
            'project_name',
            'project_description',
            'start_date',
            'end_date',
        ]
       

class TaskAddedForms(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_key',
            'employee_key',
            'task_name',
            'task_description',
            'start_date_task',
            'end_date_task',
        ]
       
class TimeAddForms(forms.ModelForm):
    class Meta:
        model = Time
        fields = [
            'date_work',
            'time_work',
        ]
       