from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from app.models import *
from app.forms import EmployeeAddedForms

def add_employee(request):
    context = {}
    if request.method == 'POST':
        form = EmployeeAddedForms(request.POST)
        if form.is_valid():
            if str(form.cleaned_data['position_key']) == 'Менеджер':
                staff = True
                superuser = False
            elif str(form.cleaned_data['position_key']) == 'Админ':
                staff = True
                superuser = True
            else:
                staff = False
                superuser = False
                
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
                is_staff=staff,
                is_superuser=superuser,
            )
            # is_staff
            emp = Employee.objects.create(
                user_key = user,
                department_key=form.cleaned_data['department_key'],
                position_key=form.cleaned_data['position_key'],
                employee_surname=form.cleaned_data['employee_surname'],
                employee_name=form.cleaned_data['employee_name'],
                employee_patronymic=form.cleaned_data['employee_patronymic'],
            )

            user.save()
            emp.save()
            return redirect(reverse('profile'))
        else:
            pass
    else:
        # added_employee.html
        form = EmployeeAddedForms()
    c = {
        'form' : form
    }
    return render(request, 'admin/added_employee.html', c)