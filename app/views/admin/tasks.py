from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from app.models import *
from app.forms import *

def add_task(request):
    context = {}
    if request.method == 'POST':
        form = TaskAddedForms(request.POST)
        if form.is_valid():
            task = Task.objects.create(
                task_key=form.cleaned_data['task_key'],
                task_name=form.cleaned_data['task_name'],
                task_description=form.cleaned_data['task_description'],
                start_date_task=form.cleaned_data['start_date_task'],
                end_date_task=form.cleaned_data['end_date_task'],
            )

            task.save()
            task.employee_key.set(form.cleaned_data['employee_key'])
            return redirect(reverse('profile'))
        else:
            pass
    else:
        # added_employee.html
        form = TaskAddedForms()
    c = {
        'form' : form
    }
    return render(request, 'admin/added_task.html', c)


# Функция изменения сотрудников на проекте(доделать)
def edit_task(request, id):
    context = {}
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskAddedForms(request.POST, instance=task)
        if form.is_valid():
            task.task_key=form.cleaned_data['task_key']
            task.task_name=form.cleaned_data['task_name']
            task.task_description=str(form.cleaned_data['task_description'])
            task.start_date_task=str(form.cleaned_data['start_date_task'])
            task.end_date_task=str(form.cleaned_data['end_date_task'])

            # Чтобы не отображался админ
            task.employee_key.set(form.cleaned_data['employee_key'])
            task.save()
            return redirect(reverse('get_tasks_for_employee', args=[str(task.task_key.id)]))
        else:
            pass
    else:
        # added_employee.html
        form = TaskAddedForms(instance=task)
    c = {
        'form' : form
    }
    return render(request, 'task/edit_task.html', c)

# Функция изменения сотрудников на проекте(доделать)
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect(reverse('profile'))