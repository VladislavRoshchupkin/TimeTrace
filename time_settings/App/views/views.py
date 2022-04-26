from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from ..models import *
from ..forms import *
import calendar
from datetime import datetime
from ..utils import Calendar


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


def get_tasks_for_employee(request, id_project):
    employee = Employee.objects.get(user_key=request.user)
    project = Project.objects.get(id=id_project)
    tasks = Task.objects.filter(employee_key=employee, task_key=project)
    times = Time.objects.filter(time_key=employee, task_key__in=tasks)
    d = {}
    for k, v in enumerate(times):
        d[k] = v
    print(d)
    c = {
        'tasks' : tasks,
        'project_name' : project.project_name,
        'times' : d
    }
    return render(request, 'tasks.html', c)


@login_required(login_url='login')
def profile(request):
    is_superuser = request.user.is_superuser or request.user.is_staff
    employee = Employee.objects.get(user_key=request.user)
    projects = Project.objects.filter(project_user_key=employee)
    dep = Department.objects.get(department_name=str(employee.department_key))

    if str(employee.position_key) == 'Менеджер':
        print('Пользователь менеджер')
    all_time = Time.objects.filter(time_key=employee)
    my_all_time = 0.0

    for at in all_time:
        my_all_time += int(at.time_work)
    
    # if my_all_time != Raiting.objects.get(raiting_key=dep).total_count:
    #     print("выполняю")
    #     rai = Raiting.objects.get(raiting_key=dep)
    #     rai.total_count = my_all_time
    #     rai.save()

    if is_superuser:
        c = {
            'employee' : Employee.objects.all(),
            'projects' : projects,
            'position' : employee.position_key,
            'is_superuser' : is_superuser
        }
    else:
        c = {
            'employee' : employee,
            'projects' : projects,
            'position' : employee.position_key,
            'is_superuser' : is_superuser
        }
    return render(request, 'profile.html', c)

# --------
# Выход из личного кабинета
def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect("/")




def time_tracking(request, id):
    current_user = Employee.objects.get(user_key=request.user)
    task = Task.objects.get(id=id)
    # times = Time.objects.filter(time_key=current_user, task_key=task)

    if request.method == 'POST':
        form = TimeAddForms(request.POST)
        if form.is_valid():
            time = Time.objects.create(
                time_key=current_user,
                task_key=task,
                date_work=form.cleaned_data['date_work'],
                time_work=form.cleaned_data['time_work'],
            )
            task.completed = True
            task.save()
            time.save()
            return redirect(reverse('profile'))
        else:
            pass
    else:
        form = TimeAddForms()

    c = {
        'form' : form,
    }
    return render(request, 'time_tracking.html', c)


def raiting(request):
    departments = Department.objects.all()
    employee = Employee.objects.filter(department_key__in=departments)

    times = Time.objects.filter(time_key__in=employee)

    for d in departments:
        employee = Employee.objects.filter(department_key=d)
        for e in employee:
            times = Time.objects.filter(time_key=e)
            temp = 0.0
            for t in times:
                temp += int(t.time_work)
                print(t.time_work)
            if not Raiting.objects.filter(raiting_key=d).exists():
                rait = Raiting.objects.create(
                    raiting_key = d,
                    total_count = temp
                )
            else:
                rai = Raiting.objects.get(raiting_key=d)
                rai.total_count = temp
                rai.save()

    raiting_all = Raiting.objects.all()
    c = {
        'departments' : departments,
        'raiting_all' : raiting_all,
    }
    return render(request, 'raiting.html', c)
    

# Функция редактирования пользователя
def edit_user(request, id):
    edit_user = Employee.objects.get(pk=id)
    if request.user.is_superuser:
        model = EditUserAdminForms
    else:
        model = EditUserForms

    if request.method == 'POST':
        form = model(request.POST, instance=edit_user)
        if form.is_valid():
            # note = form.save(commit=False)
            edit_user.employee_surname = form.cleaned_data['employee_surname']
            edit_user.employee_name = form.cleaned_data['employee_name']
            edit_user.employee_patronymic = form.cleaned_data['employee_patronymic']
            edit_user.user_key = request.user
            edit_user.save()
            return redirect('profile')
    else:
        form = model(instance=edit_user)
    context = {
                'form' : form,
    }
    return render(request, 'edit_profile.html', context=context)




# ===============================

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from ..models import *
from ..utils import Calendar

class CalendarView(generic.ListView):
    model = Time
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    form = TimeAddForms(request.POST)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse(redirect('calendar')))
    return render(request, 'cal/event.html', {'form': form})



