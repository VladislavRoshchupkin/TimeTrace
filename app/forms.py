from django import forms
from django.contrib.auth.models import User
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

class WeekendAddedForms(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'weekend_count',
        ]
        widgets = {
            'weekend_count': forms.NumberInput(attrs={'min': 0, 'max' : 365}),
        }


class ChangeTimeForms(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'status_task',
        ]

class ProjectAddedForms(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_user_key',
            'manager_key',
            'project_name',
            'project_description',
            'start_date',
            'end_date',
        ]
        widgets = {
            'project_user_key': forms.CheckboxSelectMultiple,
            'start_date' : forms.TextInput(attrs={'type': 'date'}),
            'end_date' : forms.TextInput(attrs={'type': 'date'}),
        }

class ProjectAddedFormsForAdmin(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_user_key',
            'manager_key',
            'project_name',
            'project_description',
            'start_date',
            'end_date',
        ]
        widgets = {
            'project_user_key': forms.CheckboxSelectMultiple,
            'start_date' : forms.TextInput(attrs={'type': 'date'}),
            'end_date' : forms.TextInput(attrs={'type': 'date'}),
        }
       
class ProjectEditFormsForNotAdmin(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_user_key',
            'manager_key',
            'project_name',
            'project_description',
        ]
        widgets = {
            'project_user_key': forms.CheckboxSelectMultiple,
        }

class ProjectEditFormsForNotAdmin(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_user_key',
        ]
        widgets = {
            'project_user_key': forms.CheckboxSelectMultiple,
        }


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
            # 'status_task',
        ]
        # widgets = {
        #     'status_task': forms.Select(attrs={'class': 'custom-select md-form'}),
        # }
        widgets = {
            'employee_key': forms.CheckboxSelectMultiple,
            'start_date_task' : forms.TextInput(attrs={'type': 'date'}),
            'end_date_task' : forms.TextInput(attrs={'type': 'date'}),
        }
       
class TimeAddForms(forms.ModelForm):
    class Meta:
        model = Time
        fields = [
            # 'task_key',
            'description',
            'date_work',
            'time_work',
        ]
        widgets = {
            'time_work': forms.NumberInput(attrs={'min': 0, 'max' : 24}),
        }
       
class EditUserForms(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Employee
        fields = [
            'employee_surname',
            'employee_name',
            'employee_patronymic',
        ]
       
class EditUserAdminForms(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    class Meta:
        model = Employee
        fields = [
            'user_key',
            'department_key',
            'employee_surname',
            'employee_name',
            'employee_patronymic',
            'weekend_count',
        ]
       
class SelectDepartments(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'department_name',
        ]
        widgets = {
            'department_name': forms.CheckboxSelectMultiple,
        }