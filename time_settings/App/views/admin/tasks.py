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