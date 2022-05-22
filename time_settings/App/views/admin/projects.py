import re
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

def add_project(request):
    context = {}
    if request.method == 'POST':
        form = ProjectAddedForms(request.POST)
        if form.is_valid():
            # print(f"form.cleaned_data['project_user_key'] = {form.cleaned_data['project_user_key']}")
            project = Project.objects.create(
                # project_user_key = form.cleaned_data['project_user_key'],
                manager_key=form.cleaned_data['manager_key'],
                project_name=form.cleaned_data['project_name'],
                project_description=form.cleaned_data['project_description'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
            )

            project.save()
            # project.project_user_key.set(form.cleaned_data['project_user_key'])
            return redirect(reverse('profile'))
        else:
            pass
    else:
        # added_employee.html
        form = ProjectAddedForms()
    c = {
        'form' : form
    }
    return render(request, 'admin/added_project.html', c)

# Функция изменения сотрудников на проекте(доделать)
def edit_project(request, id):
    if request.user.is_superuser:
        ModelForm = ProjectAddedForms
    else:
        ModelForm = ProjectEditFormsForNotAdmin
    context = {}
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = ModelForm(request.POST, instance=project)
        if form.is_valid():
            project.project_name=form.cleaned_data['project_name']
            project.project_description=form.cleaned_data['project_description']
            if request.user.is_superuser:

                project.start_date=str(form.cleaned_data['start_date'])
                project.end_date=str(form.cleaned_data['end_date'])
            project.project_user_key.set(form.cleaned_data['project_user_key'])
            project.save()
            return redirect(reverse('profile'))
        else:
            pass
    else:
        # added_employee.html
        form = ProjectAddedForms(instance=project)
    c = {
        'form' : form
    }
    return render(request, 'edit_project.html', c)

# Функция изменения сотрудников на проекте(доделать)
def delete_project(request, id):
    project = Project.objects.get(id=id)
    project.delete()
    return redirect(reverse('profile'))