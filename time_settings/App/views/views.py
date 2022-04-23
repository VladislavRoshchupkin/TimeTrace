import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from ..models import *


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    else:
        return redirect(reverse('login'))


# --------
# Вход в личный кабинет
def login_user(request):   
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active: # user.is_active: если пользователь активен, наверное
            login(request, user)
            return redirect(reverse("profile"))
        else:
            return redirect(reverse('login'))
    return render(request, 'auth/login.html')


def get_tasks_for_employee(request, id_task):
    employee = Employee.objects.get(user_key=request.user)
    project = Project.objects.get(id=id_task)
    tasks = Task.objects.filter(employee_key=employee, task_key=project)
    print(tasks)
    c = {
        'tasks' : tasks
    }
    return render(request, 'tasks.html', c)


@login_required(login_url='login')
def profile(request):
    employee = Employee.objects.get(user_key=request.user)
    projects = Project.objects.filter(project_user_key=employee)
    print(employee.position_key)
    c = {
        'employee' : employee,
        'projects' : projects,
    }
    return render(request, 'profile.html', c)

# --------
# Выход из личного кабинета
def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
