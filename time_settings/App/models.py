from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Department(models.Model):
    """ Класс Отдела """
    department_name = models.CharField(max_length=50, verbose_name='Название отдела')
    count_employee = models.IntegerField(verbose_name='Количество сотрудников', default=0)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'отделы'

    def __str__(self):
        return f'{self.department_name}'


class Position(models.Model):
    """ Класс Должности """
    # POSITIONS = [
    #     ('Менеджер', 'Менеджер'),
    #     ('Сотрудник', 'Сотрудник'),
    #     ('Админ', 'Админ'),
    # ]

    position_name = models.CharField(max_length=30, verbose_name='Название должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return f'{self.position_name}'


class Employee(models.Model):
    """ Класс сотрудника """
    user_key = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='К какому User относится')
    department_key = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='К какому отделу относится')
    position_key = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность',
        related_name='position')
    employee_surname= models.CharField(max_length=30, verbose_name='Фамилия')
    employee_name = models.CharField(max_length=20, verbose_name='Имя')
    employee_patronymic= models.CharField(max_length=30, verbose_name='Отчество')
    # photo = models.ImageField(verbose_name='Фотография')
    weekend_count = models.IntegerField(verbose_name='Количество выходных', blank=True, default=0)
    
    class Meta:
        verbose_name = 'Сотрудника'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.employee_surname} {self.employee_name}'


class Project(models.Model):
    """ Класс проектов """
    project_user_key = models.ManyToManyField(Employee, related_name='project_key', verbose_name='К каким сотрудникам принадллежит проект')
    project_name = models.CharField(max_length=150, verbose_name='Название проекта')
    project_description = models.TextField(max_length=250, verbose_name='Содержмое')
    start_date = models.DateTimeField(verbose_name='Предполагаемое начало выполнения')
    end_date = models.DateTimeField(verbose_name='Предполагаемый конец выполнения')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f'{self.project_name}'


class Task(models.Model):
    """ Класс задач """
    task_key = models.ForeignKey(Project, on_delete=models.CASCADE, \
        verbose_name='Какому проекту принадлежит задача')
    employee_key = models.ManyToManyField(Employee, \
        verbose_name='Какому сотруднику принадлежит задача', related_name='employee_key')
    task_name = models.CharField(max_length=50, verbose_name='Название задачи')
    task_description = models.TextField(max_length=250, verbose_name='Содержмое задачи')
    start_date_task = models.DateTimeField(verbose_name='Предполагаемое начало выполнения')
    end_date_task = models.DateTimeField(verbose_name='Предполагаемый конец выполнения')

    
    class Meta:
        verbose_name = 'задачу'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.task_key}'


class Raiting(models.Model):
    raiting_key = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='К какому отделу относится рейтинг')
    total_count = models.IntegerField(verbose_name='Общее количество наработанных часов в отделе')

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'

    def __str__(self):
        return f'{self.raiting_key}'


class Time(models.Model):
    time_key = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='К какому сотруднику принадлежит')
    """ Учет времени """
    # DAYS = [
    #     ('Понедельник', 'Понедельник'),
    #     ('Вторник', 'Вторник'),
    #     ('Среда', 'Среда'),
    #     ('Четверг', 'Четверг'),
    #     ('Пятница', 'Пятница'),
    #     ('Суббота', 'Суббота'),
    #     ('Воскресенье', 'Воскресенье'),
    # ]
    # name_of_day = models.CharField(
    #     max_length=150,
    #     choices=DAYS,
    #     verbose_name='День'
    # )

    date_work = models.DateField(verbose_name='Выбранный день работы')
    time_work = models.TimeField(verbose_name='Проработанное количество часов')


    class Meta:
        verbose_name = 'учет времени'
        verbose_name_plural = 'учеты времени'

    def __str__(self):
        return f'{self.time_key}'

    
# class Notice(models.Model):
#     notice_key = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='От ког опришло уведомление')
    