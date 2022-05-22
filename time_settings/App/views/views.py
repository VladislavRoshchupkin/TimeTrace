from time import time
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
import datetime
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.conf import settings

from ..models import Time
from ..utils import Calendar
from ..forms import TimeAddForms



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
    if request.user.is_superuser:
        c = {
        'tasks' : tasks,
        'project_name' : project.project_name,
        'times' : d
    }
    else:
        c = {
            'tasks' : tasks,
            'project_name' : project.project_name,
            'times' : d
        }
    return render(request, 'tasks.html', c)


@login_required(login_url='login')
def profile(request):
    is_super = request.user.is_superuser or request.user.is_staff
    employee = Employee.objects.get(user_key=request.user)
    projects = Project.objects.filter(project_user_key=employee)
    dep = Department.objects.get(department_name=str(employee.department_key))

  
    all_time = Time.objects.filter(time_key=employee)
    my_all_time = 0.0

    # for at in all_time:
    #     my_all_time += int(at.time_work)
    # print(my_all_time)
    # if my_all_time != Raiting.objects.get(raiting_key=dep).total_count:
    #     print("выполняю")
    #     rai = Raiting.objects.get(raiting_key=dep)
    #     rai.total_count = my_all_time
    #     rai.save()

    if request.user.is_superuser:
        c = {
            'employee' : Employee.objects.all().exclude(user_key=True),
            'profile_info' : Employee.objects.get(user_key=request.user),
            'projects' : Project.objects.all(),
            'position' : employee.position_key,
            'is_superuser' : is_super
        }
    elif request.user.is_staff:
        c = {
            'employee' : Employee.objects.all().exclude(user_key=True),
            'profile_info' : Employee.objects.get(user_key=request.user),
            'projects' : projects,
            'position' : employee.position_key,
            'is_superuser' : is_super
        }
    else:
        c = {
            'employee' : Employee.objects.filter(department_key=dep),
            'profile_info' : Employee.objects.get(user_key=request.user),
            'projects' : projects,
            'position' : employee.position_key,
            'is_superuser' : is_super
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
    events = Time.objects.filter(time_key=current_user)
    events_month = Time.objects.filter(
            time_key=current_user,
            date_work=datetime.now().date(),
        )
    
    event_list = []
    # start: '2020-09-16T16:00:00'
    for event in events:
        event_list.append(
            {
                "title": f'{event.task_key.id} - {event.task_key.task_name} - {event.time_work}ч',
                "start": event.date_work.strftime("%Y-%m-%d"),
                "end": event.date_work.strftime("%Y-%m-%d")
            }
        )

    if request.method == 'POST':
        form = TimeAddForms(request.POST)
        if form.is_valid():
            time = Time.objects.create(
                time_key=current_user,
                task_key=task,
                date_work=form.cleaned_data['date_work'],
                description=form.cleaned_data['description'],
                time_work=form.cleaned_data['time_work'],
            )
            task.save()
            time.save()
            return redirect(reverse('time_tracking', args=[id]))
        else:
            pass
    else:
        form = TimeAddForms()
    

    c = {
        "form": form, "events": event_list, "events_month": events_month
    }
    return render(request, 'time_tracking.html', c)


def raiting(request):
    employee = Employee.objects.get(user_key=request.user)
    department = employee.department_key
    
    times = Time.objects.filter(time_key=employee)

    current_department = Department.objects.get(department_name=department)

    all_employees = Employee.objects.filter(department_key=current_department)
    
    times_in_employee = []
    temp = 0.0
    d = {}
    d_superuser = {}

    for e in all_employees:
        time = Time.objects.filter(time_key=e)
        time_current = 0
        for t in time:
            temp += int(t.time_work)
            time_current += int(t.time_work) # добавляю время для каждого пользователя
        

        if not Raiting.objects.filter(raiting_key=current_department).exists():
            rait = Raiting.objects.create(
                raiting_key = current_department,
                total_count = temp
            )
        else:
            rai = Raiting.objects.get(raiting_key=current_department)
            rai.total_count = temp
            rai.save()
        times_in_employee.append(time_current)
        d[e] = time_current

    if request.user.is_superuser:
        department = Department.objects.all()

        for dep in department:
            employee = Employee.objects.filter(department_key=dep)
            for e in employee:
                time = Time.objects.filter(time_key=e)
                time_current = 0
                for t in time:
                    temp += int(t.time_work)
                    time_current += int(t.time_work) # добавляю время для каждого пользователя
                
                if not Raiting.objects.filter(raiting_key=current_department).exists():
                    rait = Raiting.objects.create(
                        raiting_key = current_department,
                        total_count = temp
                    )
                else:
                    rai = Raiting.objects.get(raiting_key=current_department)
                    rai.total_count = temp
                    rai.save()
                times_in_employee.append(time_current)
                d_superuser[dep] = employee



    if request.user.is_superuser:
        c = {
        'departments' : Department.objects.all(),
        'raiting_all' : Raiting.objects.all(),
        'all_employees' : all_employees,
        'times_in_employee' : times_in_employee,
        'time_for_employees' : d_superuser
        }
    else:
        c = {
            'departments' : department,
            'raiting_all' : Raiting.objects.get(raiting_key=current_department),
            'all_employees' : all_employees,
            'times_in_employee' : times_in_employee,
            'time_for_employees' : d
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
            user_instance = User.objects.get(username=edit_user.user_key.username)
            edit_user.employee_surname = form.cleaned_data['employee_surname']
            edit_user.employee_name = form.cleaned_data['employee_name']
            edit_user.employee_patronymic = form.cleaned_data['employee_patronymic']
            edit_user.user_key = request.user
        
            user_instance.email=form.cleaned_data['email']
            user_instance.username=form.cleaned_data['username']
            user_instance.password=make_password(form.cleaned_data['password'])
            user_instance.save()
            edit_user.save()
            
            print()
            return redirect('profile')
    else:
        form = model(instance=edit_user)
    context = {
                'form' : form,
    }
    return render(request, 'edit_profile.html', context=context)




# ===============================


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Time
    template_name = "cal/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def create_event(request):
    current_user = Employee.objects.get(user_key=request.user)
    task = Task.objects.get(id=id)
    form = TimeAddForms(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        time = Time.objects.create(
                time_key=current_user,
                task_key=task,
                date_work=form.cleaned_data['date_work'],
                time_work=form.cleaned_data['time_work'],
            )
        task.save()
        time.save()
        return redirect(reverse('profile'))

        
        # return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})





class CalendarViewNew(LoginRequiredMixin, generic.View):
    template_name = "time_tracking.html"
    form_class = TimeAddForms
    def get(self, request, *args, **kwargs):
        employee = Employee.objects.get(user_key=request.user)
        forms = self.form_class()
        events = Time.objects.filter(time_key=employee)
        events_month = Time.objects.filter(
            time_key=employee,
            date_work=datetime.now().date(),
        )
      
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.task_key.task_name,
                    "start": event.date_work.strftime("%Y-%m-%d"),
                    "end": event.date_work.strftime("%Y-%m-%d")
                }
            )


        context = {"form": forms, "events": event_list, "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)

def get_time_all(request, id):
    project = Project.objects.get(id=id)
    current_employee = Employee.objects.get(user_key=request.user)

    # if request.user.is_superuser:
    #     employees = project.project_user_key.all()
    # elif request.user.is_staff:
    #     employees = project.project_user_key.all().exclude(user_key=request.user)
    # else:
  
    employees = project.project_user_key.all().exclude(user_key=request.user) # .exclude(user_key=request.user)
    
    
    print(current_employee)
    c = {
        'project' : project,
        'time' : Time.objects.filter(time_key__in=employees),
        'employees' : employees,
        'current_employee' : current_employee,
    }
    return render(request, 'show_time.html', c)

def add_weekend(request, id):
    employee = Employee.objects.get(id=id)
    
    if request.method == 'POST':
        form = WeekendAddedForms(request.POST, instance=employee)
        if form.is_valid():
            employee.weekend_count = int(form.cleaned_data['weekend_count'])
            employee.save()
            return redirect(reverse('profile'))
    else:
        form = WeekendAddedForms(instance=employee)

    context = {
        'form' : form
    }
    return render(request, 'add_weekends.html', context)


def change_time_work(request, id):
    """ Изменение времени работы незашедшему пользователю """
    task = Task.objects.get(id=id)
    
    if request.method == 'POST':
        form = ChangeTimeForms(request.POST, instance=task)
        if form.is_valid():
            # employee.weekend_count = int(form.cleaned_data['weekend_count'])
            # employee.save()
            task.status_task = form.cleaned_data['status_task']
            task.save()
            return redirect(reverse('get_tasks_for_employee', args=[task.task_key.id]))
    else:
        form = ChangeTimeForms(instance=task)

    context = {
        'form' : form
    }
    return render(request, 'change_time_work.html', context)

